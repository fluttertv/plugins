#!/usr/bin/env python3
"""Turn upstream_check.py reports into one GitHub issue per package.

One issue per package, found by its exact title among issues carrying the
`upstream-compat` label. The body ends in a hidden fingerprint
(see upstream_check.fingerprint), and that is what keeps a daily schedule from
becoming daily noise:

  finding, no open issue           open one
  finding, open issue, same print  leave it alone — no edit, no comment
  finding, open issue, new print   rewrite the body, add a one-line comment
  finding, hand-closed issue, same print
                                   leave it closed: a maintainer closed it
                                   knowing about exactly this finding
  ok, open issue                   mark the body auto-closed, comment that it
                                   passes again, close it

A finding that changes after a maintainer closed the issue (a newer upstream
major, a different failing step) opens a fresh issue, because the closing
decision was about something else. An issue this script closed itself never
silences anything: the same finding coming back later is a new regression, so
it opens a fresh issue. The AUTO_CLOSED marker in the body is how the two kinds
of closed issue are told apart.

Usage:
    upstream_issues.py <reports-dir> --repo owner/name [--dry-run]

Needs `gh` authenticated with issues: write (GH_TOKEN in Actions).
"""

import argparse
import glob
import json
import re
import subprocess
import sys

LABEL = "upstream-compat"
LABEL_COLOR = "fbca04"
LABEL_DESC = "A newer upstream package or Flutter stable breaks or excludes a plugin"
MARKER = re.compile(r"<!-- upstream-compat:fingerprint=([0-9a-f]+) -->")
AUTO_CLOSED = "<!-- upstream-compat:auto-closed -->"
BODY_LIMIT = 60000  # GitHub rejects issue bodies over 65536 characters.

HEADLINES = {
    "broken": "fails **within its current constraints** — users are affected now",
    "major-breaks": "is excluded by a new upstream major, and moving to it **fails**",
    "lag": "is excluded by a new upstream major; moving to it **passes**, so "
           "widening the constraint is the fix",
}


def title_for(package):
    return f"Upstream compatibility: {package}"


def gh(args, input_text=None):
    """Run gh. Callers guard every write with `dry_run`; only reads get here
    unguarded."""
    proc = subprocess.run(["gh", *args], input=input_text, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def fence(text):
    return "```text\n" + text.replace("```", "``​`") + "\n```"


def render(report):
    pkg = report["package"]
    tools = report.get("tools") or {}
    out = [f"`{pkg}` {HEADLINES[report['status']]}.", ""]
    out.append(f"- Flutter {tools.get('flutter', '?')} (stable), "
               f"Dart {tools.get('dart', '?')}")
    if report.get("run_url"):
        out.append(f"- Run: {report['run_url']}")
    out.append("")

    if report["outdated"]:
        out += ["### Upstream releases outside our constraints", "",
                "| dependency | our constraint | newest allowed | newest release |",
                "|---|---|---|---|"]
        for o in report["outdated"]:
            out.append(f"| `{o['package']}` | `{o['constraint']}` | "
                       f"{o['upgradable'] or '—'} | **{o['latest']}** |")
        out.append("")

    names = {"current": "Within current constraints (`flutter pub upgrade`)",
             "major": "Across majors (`flutter pub upgrade --major-versions`)"}
    for key in ("current", "major"):
        leg = report["legs"].get(key)
        if not leg:
            continue
        verdict = "passes" if leg["passed"] else "**fails**"
        out += [f"### {names[key]} — {verdict}", ""]
        if leg.get("constraint_changes"):
            out.append("Constraint changes pub chose:")
            out.append("")
            for name, ch in leg["constraint_changes"].items():
                out.append(f"- `{name}`: `{ch['from']}` → `{ch['to']}`")
            out.append("")
        if leg.get("resolved"):
            resolved = ", ".join(f"`{k}` {v}" for k, v in sorted(leg["resolved"].items()))
            out += [f"Resolved: {resolved}", ""]
        for step in leg["steps"]:
            out.append(f"- {'✅' if step['ok'] else '❌'} `{step['name']}`")
        failed = next((s for s in leg["steps"] if not s["ok"]), None)
        if failed:
            out += ["", "<details><summary>Output of the failing step</summary>",
                    "", fence(failed["log"]), "", "</details>"]
        out.append("")

    out += ["---",
            "Filed by the scheduled **Upstream compatibility** workflow. It "
            "updates this issue only when the finding changes, and closes it "
            "once the package passes again. Closing it by hand silences this "
            "exact finding; a different one opens a new issue.",
            f"<!-- upstream-compat:fingerprint={report['fingerprint']} -->"]
    body = "\n".join(out)
    if len(body) > BODY_LIMIT:
        body = body[:BODY_LIMIT] + "\n\n[truncated — see the run log]\n" + out[-1]
    return body


def existing(repo, package):
    """(open_issue, newest_closed_issue) with this package's exact title."""
    raw = gh(["issue", "list", "--repo", repo, "--label", LABEL, "--state", "all",
              "--limit", "500", "--json", "number,title,state,body,closedAt"])
    issues = [i for i in json.loads(raw or "[]") if i["title"] == title_for(package)]
    open_ = next((i for i in issues if i["state"] == "OPEN"), None)
    closed = sorted((i for i in issues if i["state"] != "OPEN"),
                    key=lambda i: i.get("closedAt") or "", reverse=True)
    return open_, (closed[0] if closed else None)


def print_of(issue):
    match = MARKER.search((issue or {}).get("body") or "")
    return match.group(1) if match else None


def auto_closed(issue):
    return AUTO_CLOSED in ((issue or {}).get("body") or "")


def sync(repo, report, dry_run):
    pkg, status = report["package"], report["status"]
    open_, closed = existing(repo, pkg)
    if status == "ok":
        if open_:
            print(f"{pkg}: passing again — closing #{open_['number']}")
            if not dry_run:
                body = (open_.get("body") or "").replace(AUTO_CLOSED, "").rstrip()
                gh(["issue", "edit", str(open_["number"]), "--repo", repo,
                    "--body-file", "-"], input_text=f"{body}\n{AUTO_CLOSED}")
                gh(["issue", "close", str(open_["number"]), "--repo", repo,
                    "--comment", "Passes again against the newest upstream "
                    f"releases and Flutter stable ({report.get('run_url') or 'scheduled run'}). "
                    "Closing."])
        else:
            print(f"{pkg}: ok")
        return
    body = render(report)
    fp = report["fingerprint"]
    if open_:
        if print_of(open_) == fp:
            if auto_closed(open_):
                # Reopened by hand after an auto-close: drop the marker so that
                # closing it by hand again does silence this finding.
                print(f"{pkg}: {status}, unchanged — clearing the auto-closed "
                      f"marker on reopened #{open_['number']}")
                if not dry_run:
                    gh(["issue", "edit", str(open_["number"]), "--repo", repo,
                        "--body-file", "-"], input_text=body)
                return
            print(f"{pkg}: {status}, unchanged — #{open_['number']} left alone")
            return
        print(f"{pkg}: {status}, finding changed — updating #{open_['number']}")
        if not dry_run:
            gh(["issue", "edit", str(open_["number"]), "--repo", repo,
                "--body-file", "-"], input_text=body)
            gh(["issue", "comment", str(open_["number"]), "--repo", repo, "--body",
                f"Finding changed (now `{status}`); the description is updated."])
        return
    if closed and print_of(closed) == fp and not auto_closed(closed):
        print(f"{pkg}: {status}, same finding as hand-closed "
              f"#{closed['number']} — not reopening")
        return
    print(f"{pkg}: {status} — opening an issue")
    if dry_run:
        print(body)
        return
    gh(["issue", "create", "--repo", repo, "--title", title_for(pkg),
        "--label", LABEL, "--body-file", "-"], input_text=body)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("reports")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--dry-run", action="store_true",
                        help="read issues, print what would change, write nothing")
    opts = parser.parse_args()

    paths = sorted(glob.glob(f"{opts.reports}/**/*.json", recursive=True))
    if not paths:
        print("error: no reports found — refusing to treat that as all-clear",
              file=sys.stderr)
        return 1
    if not opts.dry_run:
        gh(["label", "create", LABEL, "--repo", opts.repo, "--color", LABEL_COLOR,
            "--description", LABEL_DESC, "--force"])
    errors = 0
    for path in paths:
        with open(path, encoding="utf-8") as handle:
            report = json.load(handle)
        try:
            sync(opts.repo, report, opts.dry_run)
        except RuntimeError as exc:
            # Keep going: one package's API hiccup must not stop the rest.
            print(f"error: {report['package']}: {exc}", file=sys.stderr)
            errors += 1
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
