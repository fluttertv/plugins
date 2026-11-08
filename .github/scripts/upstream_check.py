#!/usr/bin/env python3
"""Check one package against the newest upstream releases and Flutter.

Each *_tvos package federates an upstream plugin through its platform
interface (shared_preferences_platform_interface, url_launcher_platform_
interface, ...), and its example depends on the app-facing upstream package.
Upstream ships on its own schedule, and three kinds of release break us without
any commit here:

  broken        Something inside our constraints already fails: a minor
                release of a platform interface added an abstract member, or a
                new Flutter stable rejects our code. Users hit this today.

  major-breaks  A new major is out that our constraint excludes, and moving to
                it fails resolution, analysis or tests. Porting work needed.

  lag           A new major is out that our constraint excludes, and moving to
                it passes. Widening the constraint is the whole fix — but until
                then, an app on the new upstream major cannot resolve us.

A package with none of these is `ok`. The script never edits the repository:
both legs run on scratch copies of packages/ (the whole tree, because
pubspec_overrides.yaml points at siblings such as ../firebase_core_tvos).

It writes <out>/<package>.json for upstream_issues.py to turn into issues. Its
exit code is about the tooling, not the findings: 0 whenever a report was
written, including for a broken package, so one package's breakage cannot hide
another's. Non-zero means no trustworthy report exists, and the workflow fails
loudly instead of filing an issue about a network blip: a resolve step that
fails with pub's network errors (pub.dev unreachable, socket errors, 5xx) is a
tooling failure, never a finding.

Usage:
    upstream_check.py <repo-root> <package> --out <dir>
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_repo import load_yaml  # noqa: E402

LOG_TAIL = 80
STEP_TIMEOUT = 20 * 60

# pub's own wording when it could not talk to the package server. A resolve
# step that fails with one of these says nothing about our package.
NETWORK_ERROR = re.compile(
    r"Got socket error|SocketException|Failed host lookup|HandshakeException|"
    r"Connection (?:refused|reset|closed|timed out)|"
    r"pub\.dev is having some trouble|having some trouble connecting|"
    r"Server error|Could not resolve URL|Network is unreachable|"
    r"TimeoutException",
    re.IGNORECASE,
)


class ToolingError(Exception):
    """The run cannot produce a trustworthy report (network, pub.dev down)."""


# Ignored when copying packages/ to scratch: build output and resolution state
# that would make a scratch run differ from a fresh checkout.
COPY_IGNORE = shutil.ignore_patterns(
    ".dart_tool", "build", "pubspec.lock", ".flutter-plugins",
    ".flutter-plugins-dependencies", "Pods", ".symlinks", "DerivedData",
)


def run_rc(cmd, cwd):
    """(exit code, combined output); the code is None when the command timed
    out or could not start. Never raises for a failing command."""
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, timeout=STEP_TIMEOUT,
        )
        return proc.returncode, proc.stdout
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        return None, out + f"\n[timed out after {STEP_TIMEOUT}s]"
    except OSError as exc:
        return None, f"[could not run {cmd[0]}: {exc}]"


def run(cmd, cwd):
    """(ok, combined output). Never raises for a failing command."""
    code, out = run_rc(cmd, cwd)
    return code == 0, out


# pub's exit code for "the package server could not be reached" (EX_UNAVAILABLE).
EXIT_UNAVAILABLE = 69


def resolve(cmd, cwd):
    """run() for a pub command that talks to the package server. A failure
    caused by the network raises ToolingError instead of becoming a step:
    exit code 69 is pub saying so outright, and the wording check catches the
    paths (flutter's wrapper, older pubs) that exit 1 for the same cause."""
    code, out = run_rc(cmd, cwd)
    if code != 0 and (code == EXIT_UNAVAILABLE or NETWORK_ERROR.search(out)):
        raise ToolingError(f"{' '.join(cmd)} in {cwd} could not reach the "
                           f"package server (exit {code}):\n" + tail(out, 20))
    return code == 0, out


def tail(text, n=LOG_TAIL):
    lines = text.rstrip().splitlines()
    if len(lines) <= n:
        return "\n".join(lines)
    return f"[... {len(lines) - n} earlier lines omitted]\n" + "\n".join(lines[-n:])


def hosted_deps(pubspec_path, section="dependencies"):
    """{name: constraint} for hosted deps in a section, minus overridden ones.

    sdk:, path: and git: dependencies are not ours to upgrade, and neither is
    anything pubspec_overrides.yaml pins to a sibling — its "latest" is
    whatever the sibling directory says.
    """
    pubspec, err = load_yaml(pubspec_path)
    if err or not isinstance(pubspec, dict):
        return {}
    overrides, _ = load_yaml(os.path.join(os.path.dirname(pubspec_path),
                                          "pubspec_overrides.yaml"))
    overridden = set()
    if isinstance(overrides, dict):
        overridden = set((overrides.get("dependency_overrides") or {}).keys())
    overridden |= set((pubspec.get("dependency_overrides") or {}).keys())
    out = {}
    for name, spec in (pubspec.get(section) or {}).items():
        if name in overridden:
            continue
        if isinstance(spec, str) or spec is None:
            out[name] = spec or "any"
        elif isinstance(spec, dict) and not ({"sdk", "path", "git"} & spec.keys()):
            out[name] = spec.get("version", "any")
    return out


def outdated(pkg_dir):
    """Direct hosted deps whose newest release our own constraint excludes.

    `pub outdated` supplies `latest`, the newest stable release (prereleases
    are not counted). A row needs our declared constraint to exclude it — see
    excludes() for why `upgradable != latest` is not the test.
    """
    ok, out = resolve(["flutter", "pub", "outdated", "--json",
                       "--no-dev-dependencies"], pkg_dir)
    if not ok:
        return None, out
    start = out.find("{")
    try:
        data = json.loads(out[start:]) if start >= 0 else {}
    except json.JSONDecodeError:
        return None, out
    wanted = hosted_deps(os.path.join(pkg_dir, "pubspec.yaml"))
    rows = []
    for row in data.get("packages", []):
        name = row.get("package")
        if name not in wanted:
            continue
        upgradable = (row.get("upgradable") or {}).get("version")
        latest = (row.get("latest") or {}).get("version")
        if latest and excludes(wanted[name], latest):
            rows.append({"package": name, "constraint": wanted[name],
                         "upgradable": upgradable, "latest": latest})
    return rows, out


def resolved_versions(pkg_dir, names):
    """{name: version} from pubspec.lock for the given names."""
    lock, _ = load_yaml(os.path.join(pkg_dir, "pubspec.lock"))
    pkgs = (lock or {}).get("packages") or {} if isinstance(lock, dict) else {}
    return {n: (pkgs.get(n) or {}).get("version") for n in names if n in pkgs}


def checks(pkg_dir, steps):
    """analyze + test for the package, then resolve + analyze its example.

    Mirrors the CI `package` job so a red here means what a red there means.
    Appends to `steps`; returns False at the first failure.
    """
    plan = [("dart analyze lib", ["dart", "analyze", "lib"], pkg_dir)]
    test_dir = os.path.join(pkg_dir, "test")
    if os.path.isdir(test_dir):
        plan.append(("dart analyze test", ["dart", "analyze", "test"], pkg_dir))
        has_tests = any(f.endswith("_test.dart")
                        for _, _, files in os.walk(test_dir) for f in files)
        if has_tests:
            plan.append(("flutter test", ["flutter", "test"], pkg_dir))
    for name, cmd, cwd in plan:
        ok, out = run(cmd, cwd)
        steps.append({"name": name, "ok": ok, "log": tail(out)})
        if not ok:
            return False
    return True


def example_checks(example_dir, steps, major):
    """Resolve the example — against the newest upstream majors when `major`.

    The example is the only place the app-facing upstream package appears
    (url_launcher, firebase_auth, ...). Upgrading it across majors is how a
    new app-facing major whose platform-interface requirement we exclude shows
    up: the resolve fails even though the plugin itself analyses clean.
    """
    if not os.path.isfile(os.path.join(example_dir, "pubspec.yaml")):
        return True
    deps = sorted(hosted_deps(os.path.join(example_dir, "pubspec.yaml")))
    cmd = ["flutter", "pub", "upgrade"]
    if major and deps:
        cmd += ["--major-versions", *deps]
    ok, out = resolve(cmd, example_dir)
    steps.append({"name": "example: " + " ".join(cmd[1:]), "ok": ok,
                  "log": tail(out)})
    if not ok:
        return False
    if not os.path.isdir(os.path.join(example_dir, "lib")):
        return True
    ok, out = run(["dart", "analyze", "lib"], example_dir)
    steps.append({"name": "example: dart analyze lib", "ok": ok, "log": tail(out)})
    return ok


VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+[0-9A-Za-z.-]+)?$")
BOUND = re.compile(r"(>=|<=|>|<)\s*([0-9][0-9A-Za-z.+-]*)")


def version_key(text):
    """Comparable key for a pub version, or None. A prerelease sorts below
    its release; build metadata does not matter for constraint checks."""
    m = VERSION.match(text.strip())
    if not m:
        return None
    major, minor, patch, pre = m.groups()
    return (int(major), int(minor), int(patch), 0 if pre else 1, pre or "")


def excludes(constraint, version):
    """True when our declared `constraint` does not allow `version`.

    This, not `upgradable != latest`, is the test for "a constraint of ours
    holds us back". `pub outdated` also reports a dependency as not
    upgradable to latest when the SDK pins it (meta, collection) or another
    package caps it, and those are not ours to widen — the current leg already
    tests whatever pub can resolve. Handles what pubspecs here use: any,
    ^x.y.z, exact versions and >=/>/</<= ranges. A form it cannot read counts
    as excluding, so an odd constraint gets looked at rather than ignored.
    """
    want = version_key(version)
    if want is None:
        return False
    c = (constraint or "any").strip().strip("'\"")
    if c == "any":
        return False
    if c.startswith("^"):
        low = version_key(c[1:])
        if low is None:
            return True
        high = (low[0] + 1, 0, 0, 0, "") if low[0] > 0 else \
            (0, low[1] + 1, 0, 0, "")
        return not (low <= want < high)
    exact = version_key(c)
    if exact is not None:
        return exact[:3] != want[:3]
    bounds = BOUND.findall(c)
    if not bounds or BOUND.sub("", c).strip():
        return True
    for op, text in bounds:
        key = version_key(text)
        if key is None:
            return True
        ok = {">=": want >= key, ">": want > key,
              "<=": want <= key, "<": want < key}[op]
        if not ok:
            return True
    return False


def same_line(resolved, latest):
    """True when `resolved` is on `latest`'s caret line (^latest would allow
    it): same major, or same minor below 1.0.0."""
    def parts(v):
        try:
            return [int(x) for x in re.split(r"[.+-]", v)[:3]]
        except (ValueError, TypeError):
            return None
    a, b = parts(resolved), parts(latest)
    if not a or not b:
        return resolved == latest
    return a[:2] == b[:2] if b[0] == 0 else a[0] == b[0]


def caret_line(version):
    """The caret line a version starts: "8" for 8.0.2, "0.5" for 0.5.3.

    Fingerprints and step names use this rather than the full version, so an
    upstream patch or minor on the same line does not count as a new finding.
    """
    parts = re.split(r"[.+-]", version or "")
    if len(parts) >= 2 and parts[0] == "0":
        return f"0.{parts[1]}"
    return parts[0] if parts and parts[0] else str(version)


def force_newest(pkg_dir, rows, steps):
    """Make sure the major leg really tests the new majors.

    `pub upgrade --major-versions` is best-effort: when another constraint
    holds a dependency back, it keeps the old major and says only "No changes
    to pubspec.yaml!" — and the leg would then pass having tested nothing new.
    Measured on firebase_auth_tvos: firebase_auth stayed on 6.x because the
    sibling firebase_core_tvos pins firebase_core to the previous major. So for
    every dependency that did not reach its newest line, ask for it outright
    with `pub add name:^latest`. Either that resolves and the checks below run
    against it, or it fails with pub's own explanation of what blocks it,
    which is the finding.
    """
    resolved = resolved_versions(pkg_dir, [r["package"] for r in rows])
    for row in rows:
        have = resolved.get(row["package"])
        if have and same_line(have, row["latest"]):
            continue
        spec = f"{row['package']}:^{row['latest']}"
        ok, out = resolve(["flutter", "pub", "add", spec], pkg_dir)
        # Exact versions go in the log, not the name: the name feeds the issue
        # fingerprint, and every upstream patch would otherwise rewrite it.
        steps.append({"name": f"pub add {row['package']} "
                              f"(newest line, {caret_line(row['latest'])}.x)",
                      "ok": ok,
                      "log": f"[pub add {spec}; pub upgrade --major-versions "
                             f"kept {have}]\n" + tail(out)})
        if not ok:
            return False
    return True


def leg(repo, package, major, rows=()):
    """Run one leg on a fresh scratch copy. Returns the leg's report."""
    scratch = tempfile.mkdtemp(prefix=f"upstream-{package}-")
    try:
        shutil.copytree(os.path.join(repo, "packages"),
                        os.path.join(scratch, "packages"), ignore=COPY_IGNORE)
        pkg_dir = os.path.join(scratch, "packages", package)
        pubspec = os.path.join(pkg_dir, "pubspec.yaml")
        before = hosted_deps(pubspec)
        steps = []
        cmd = ["flutter", "pub", "upgrade"]
        if major and before:
            # Named deps only: a bare --major-versions would also cross-major
            # dev_dependencies such as flutter_lints, and a new lint set is not
            # an upstream compatibility problem.
            cmd += ["--major-versions", *sorted(before)]
        ok, out = resolve(cmd, pkg_dir)
        steps.append({"name": " ".join(cmd[1:]), "ok": ok, "log": tail(out)})
        if ok and major:
            ok = force_newest(pkg_dir, rows, steps)
        after = hosted_deps(pubspec)
        changes = {n: {"from": before[n], "to": after.get(n)}
                   for n in before if after.get(n) != before[n]}
        passed = ok and checks(pkg_dir, steps) and \
            example_checks(os.path.join(pkg_dir, "example"), steps, major)
        return {
            "passed": passed,
            "constraint_changes": changes,
            "resolved": resolved_versions(pkg_dir, before),
            "steps": steps,
        }
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def tool_versions():
    ok, out = run(["flutter", "--version", "--machine"], ".")
    if not ok:
        return {}
    try:
        data = json.loads(out[out.find("{"):])
    except (ValueError, json.JSONDecodeError):
        return {}
    return {"flutter": data.get("frameworkVersion"),
            "dart": data.get("dartSdkVersion")}


def fingerprint(report):
    """What has to change before an open issue is worth touching again.

    Deliberately excludes logs, which carry timings and paths, the Flutter
    version, and exact upstream versions — every new stable or upstream patch
    would otherwise rewrite every open issue even when the failure is the
    same. Upstream releases count by caret line, so a new *major* is a new
    finding and 8.0.1 → 8.0.2 is not. A new stable that *changes* the outcome
    changes the failing step, which is in here.
    """
    def failing(leg_report):
        if not leg_report:
            return None
        return next((s["name"] for s in leg_report["steps"] if not s["ok"]), None)

    key = {
        "status": report["status"],
        "outdated": sorted((o["package"], caret_line(o["latest"]))
                           for o in report["outdated"]),
        "current": failing(report["legs"].get("current")),
        "major": failing(report["legs"].get("major")),
    }
    blob = json.dumps(key, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("root")
    parser.add_argument("package")
    parser.add_argument("--out", required=True)
    opts = parser.parse_args()
    repo = os.path.abspath(opts.root)
    pkg_dir = os.path.join(repo, "packages", opts.package)
    if not os.path.isfile(os.path.join(pkg_dir, "pubspec.yaml")):
        print(f"error: {pkg_dir}/pubspec.yaml not found", file=sys.stderr)
        return 2

    try:
        return check(repo, opts)
    except ToolingError as exc:
        print(f"error: no trustworthy report for {opts.package}: {exc}",
              file=sys.stderr)
        return 4


def check(repo, opts):
    # `pub outdated` needs a resolution; do it on scratch too, so the checkout
    # is left exactly as found.
    scratch = tempfile.mkdtemp(prefix=f"outdated-{opts.package}-")
    try:
        shutil.copytree(os.path.join(repo, "packages"),
                        os.path.join(scratch, "packages"), ignore=COPY_IGNORE)
        sdir = os.path.join(scratch, "packages", opts.package)
        ok, out = resolve(["flutter", "pub", "get"], sdir)
        rows, out2 = outdated(sdir) if ok else (None, out)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    legs = {"current": leg(repo, opts.package, major=False)}
    if rows is None:
        # Could not even resolve within the constraints. That is a real
        # finding (e.g. a new Flutter whose SDK constraint excludes us) as long
        # as the current leg failed the same way; if the current leg passed,
        # this was flakiness and no report is trustworthy.
        if legs["current"]["passed"]:
            print("error: pub outdated failed but the current leg passed:\n"
                  + tail(out2), file=sys.stderr)
            return 3
        rows = []
    if rows:
        legs["major"] = leg(repo, opts.package, major=True, rows=rows)

    if not legs["current"]["passed"]:
        status = "broken"
    elif rows and not legs["major"]["passed"]:
        status = "major-breaks"
    elif rows:
        status = "lag"
    else:
        status = "ok"

    report = {
        "package": opts.package,
        "status": status,
        "tools": tool_versions(),
        "outdated": rows,
        "legs": legs,
        "run_url": os.environ.get("RUN_URL"),
    }
    report["fingerprint"] = fingerprint(report)
    os.makedirs(opts.out, exist_ok=True)
    with open(os.path.join(opts.out, f"{opts.package}.json"), "w",
              encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    print(f"{opts.package}: {status} (fingerprint {report['fingerprint']})")
    for name, rep in legs.items():
        for step in rep["steps"]:
            print(f"  [{name}] {'ok  ' if step['ok'] else 'FAIL'} {step['name']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
