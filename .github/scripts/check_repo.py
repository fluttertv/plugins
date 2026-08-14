#!/usr/bin/env python3
"""Structural checks over packages/ that need neither Flutter nor a network.

These are the invariants nobody re-reads a checklist for. Each one has been
broken at least once, or was caught only because a human happened to look:

  R1  every package has a row in the root README's plugin table
      Missed on the firebase_performance_tvos port. AUTHORING.md makes it a
      step of its own, and without the row the package is undiscoverable from
      the repo index.

  R2  pubspec version == podspec s.version == the newest CHANGELOG heading
      path_provider_tvos and sqflite_tvos had already drifted. The podspec
      version is inert while pods resolve by :path, so nothing surfaces it.

  R3  the files a package cannot ship without

  R4  a committed pubspec_overrides.yaml does not reach the published archive
      `dart pub publish` drops the package's own root override on its own, but
      NOT a nested one: example/pubspec_overrides.yaml ships unless .pubignore
      excludes it. That is cosmetic rather than fatal — a consumer resolving a
      hosted dependency ignores that dependency's overrides — but the archive
      should describe what consumers actually get.

  R5  the tvOS platform block declares a pluginClass
      AUTHORING.md: the CLI discovers the plugin through
      flutter.plugin.platforms.tvos. Miss it and the plugin silently does not
      register, giving MissingPluginException at the first call, at runtime, on
      a device, with nothing pointing at the cause. Every package here is
      native-backed, so pluginClass is the field that has to be present.

Every rule reports the package it failed on and how to fix it, and a run
reports what it *skipped* as loudly as what it rejected: a check that quietly
declines to run is the failure mode this file exists to prevent.

Usage:
    check_repo.py [repo-root]        run the checks
    check_repo.py --list [root]      print package names, one per line
    check_repo.py --selftest         verify every rule fires, and does not

Exits non-zero if any check fails.
"""

import os
import re
import shutil
import sys
import tempfile

import yaml

REQUIRED_FILES = ["pubspec.yaml", "README.md", "CHANGELOG.md", "LICENSE"]


def load_yaml(path):
    """Parsed YAML, or a (None, reason) pair. Never raises."""
    try:
        with open(path, encoding="utf-8") as handle:
            return yaml.safe_load(handle), None
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        return None, str(exc).split("\n")[0]


def read_text(path):
    """File contents, or a (None, reason) pair. Never raises."""
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read(), None
    except (OSError, UnicodeDecodeError) as exc:
        return None, str(exc).split("\n")[0]


def tvos_plugin_class(pubspec):
    """flutter.plugin.platforms.tvos.pluginClass, or None.

    Parsed rather than scanned. The hand-rolled version walked out of the
    `tvos:` block into whichever platform followed it and returned *that*
    platform's class, so a package declaring only `ios: pluginClass:` passed
    the one rule whose failure is invisible until an app calls the plugin.
    """
    if not isinstance(pubspec, dict):
        return None
    node = pubspec.get("flutter")
    for key in ("plugin", "platforms", "tvos"):
        if not isinstance(node, dict):
            return None
        node = node.get(key)
    if not isinstance(node, dict):
        return None
    value = node.get("pluginClass")
    return value if isinstance(value, str) and value.strip() else None


def readme_table_rows(readme):
    """The set of `packages/<name>` links inside the README's plugin table.

    Scoped to table rows so a passing mention in prose cannot satisfy R1 — the
    rule is about the index a reader browses, not about the string appearing
    somewhere in the file.
    """
    rows = set()
    for line in readme.split("\n"):
        if not line.lstrip().startswith("|"):
            continue
        rows.update(re.findall(r"\(packages/([A-Za-z0-9_]+)/?\)", line))
    return rows


def pubignore_excludes(text, name):
    """True if `name` is excluded by this .pubignore.

    Line-wise, ignoring comments and rejecting negations: a substring test
    passes on `# pubspec_overrides.yaml` and, worse, on `!pubspec_overrides`,
    which forces the file *in*.
    """
    for raw in text.split("\n"):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("!"):
            continue
        if line.rstrip("/").endswith(name):
            return True
    return False


def newest_changelog_version(text):
    """The first `## ` heading's version, or (None, heading).

    The first heading of any kind, not the first numeric one: matching on a
    leading digit skipped `## Unreleased` and validated the released entry
    underneath it, so a changelog whose top section had no version passed.
    """
    match = re.search(r"^##\s+(.+?)\s*$", text, re.M)
    if not match:
        return None, None
    heading = match.group(1).strip()
    version = re.match(r"\[?([0-9][^\]\s]*)\]?", heading)
    return (version.group(1) if version else None), heading


def podspec_version(text):
    """`s.version` from a podspec, ignoring commented-out lines."""
    match = re.search(r"^\s*s\.version\s*=\s*['\"]([^'\"]+)['\"]", text, re.M)
    return match.group(1) if match else None


def discover(pkg_root):
    """Every directory under packages/. Not "every directory with a pubspec" —
    that made a package with a misnamed pubspec vanish from the run instead of
    failing it, and silently disagreed with the workflow's own matrix."""
    if not os.path.isdir(pkg_root):
        return []
    return sorted(
        d for d in os.listdir(pkg_root)
        if os.path.isdir(os.path.join(pkg_root, d)) and not d.startswith(".")
    )


def check(root):
    """Returns (failures, packages). Each failure is (rule, package, message, fix)."""
    pkg_root = os.path.join(root, "packages")
    packages = discover(pkg_root)
    failures = []

    def fail(rule, pkg, msg, fix=None):
        failures.append((rule, pkg, msg, fix))

    if not packages:
        fail("R0", "-", f"no package directories under {pkg_root}",
             "an empty run would report success having checked nothing")
        return failures, packages

    readme, err = read_text(os.path.join(root, "README.md"))
    table = readme_table_rows(readme) if readme is not None else None
    if table is None:
        fail("R0", "-", f"cannot read the root README.md ({err})",
             "R1 cannot run without it, so this is fatal rather than skipped")

    for pkg in packages:
        d = os.path.join(pkg_root, pkg)

        # R3 — required files.
        for name in REQUIRED_FILES:
            if not os.path.isfile(os.path.join(d, name)):
                fail("R3", pkg, f"{name} is missing")

        # R1 — a row in the README's plugin table.
        if table is not None and pkg not in table:
            fail("R1", pkg, "no row in the root README's plugin table",
                 f"add a row linking packages/{pkg} under '## List of plugins'")

        pubspec_path = os.path.join(d, "pubspec.yaml")
        pubspec, err = load_yaml(pubspec_path)
        if pubspec is None:
            fail("R3", pkg, f"pubspec.yaml is unreadable or invalid ({err})")
            continue  # nothing below can be judged without it
        if not isinstance(pubspec, dict):
            fail("R3", pkg, "pubspec.yaml is not a YAML mapping")
            continue

        version = pubspec.get("version")
        version = str(version).strip() if version is not None else None
        if not version:
            fail("R2", pkg, "pubspec.yaml declares no version")

        # R2 — podspec. Presence is checked whether or not the version parsed;
        # nesting it under the version check hid a missing podspec behind an
        # unrelated failure and cost a round-trip through CI to discover.
        tvos_dir = os.path.join(d, "tvos")
        podspecs = (
            sorted(f for f in os.listdir(tvos_dir) if f.endswith(".podspec"))
            if os.path.isdir(tvos_dir) else []
        )
        if not podspecs:
            fail("R3", pkg, "tvos/ ships no .podspec")
        for spec in podspecs:
            text, err = read_text(os.path.join(tvos_dir, spec))
            if text is None:
                fail("R3", pkg, f"{spec} is unreadable ({err})")
                continue
            declared = podspec_version(text)
            if declared is None:
                fail("R2", pkg, f"{spec} declares no s.version")
            elif version and declared != version:
                fail("R2", pkg, f"{spec} says {declared}, pubspec.yaml says {version}",
                     f"set s.version = '{version}'")

        # R2 — changelog.
        changelog, err = read_text(os.path.join(d, "CHANGELOG.md"))
        if changelog is None:
            if os.path.exists(os.path.join(d, "CHANGELOG.md")):
                fail("R3", pkg, f"CHANGELOG.md is unreadable ({err})")
        else:
            newest, heading = newest_changelog_version(changelog)
            if heading is None:
                fail("R2", pkg, "CHANGELOG.md has no `## ` heading")
            elif newest is None:
                fail("R2", pkg, f"CHANGELOG.md's newest heading is '{heading}', not a version",
                     f"the top section should be `## {version or '<version>'}`")
            elif version and newest != version:
                fail("R2", pkg, f"CHANGELOG.md starts at {newest}, pubspec.yaml says {version}",
                     f"add a `## {version}` entry at the top")

        # R4 — a nested override must not reach the archive.
        nested = os.path.join(d, "example", "pubspec_overrides.yaml")
        if os.path.isfile(nested):
            pubignore, _ = read_text(os.path.join(d, ".pubignore"))
            if pubignore is None or not pubignore_excludes(pubignore, "pubspec_overrides.yaml"):
                fail("R4", pkg,
                     "example/pubspec_overrides.yaml is committed but not excluded by .pubignore",
                     "add `pubspec_overrides.yaml` to .pubignore, or delete the "
                     "override if the dependency it pins is now published")

        # R5 — the tvOS plugin class.
        if not tvos_plugin_class(pubspec):
            fail("R5", pkg,
                 "declares no flutter.plugin.platforms.tvos.pluginClass",
                 "without it the CLI never registers the plugin — "
                 "MissingPluginException at the first call")

    return failures, packages


def report(root):
    failures, packages = check(root)
    print(f"Checked {len(packages)} package(s) under packages/\n")
    if not failures:
        print("  OK — README rows, versions, required files, overrides and "
              "tvOS plugin classes all consistent.")
        return 0
    width = max(len(p) for _, p, _, _ in failures)
    for rule, pkg, msg, fix in failures:
        print(f"  {rule}  {pkg.ljust(width)}  {msg}")
        if fix:
            print(f"      → {fix}")
    print(f"\n{len(failures)} problem(s). Each rule's rationale is in the "
          f"docstring at the top of .github/scripts/check_repo.py.")
    return 1


# --- Self-test -------------------------------------------------------------
#
# The rules are only half the file; the other half is the failure paths, and on
# a green tree none of them execute. Measured with `trace --count --missing`,
# an earlier revision ran 67 of 105 lines on a passing run — every fail() site
# was cold, including the one inside fail() itself. Four of five rules were
# silently passing trees they were written to reject, and nothing could have
# told us.
#
# So each case asserts in BOTH directions. Asserting only "the rule fires on a
# bad tree" would have caught none of those four: every one was a silent pass
# on a tree that superficially looked compliant.

GOOD_PUBSPEC = """\
name: {name}
version: 0.0.1
flutter:
  plugin:
    platforms:
      tvos:
        pluginClass: GoodPlugin
"""


def _fixture(root, name="widget_tvos", **overrides):
    """A minimal package that passes every rule, then selectively broken."""
    d = os.path.join(root, "packages", name)
    os.makedirs(os.path.join(d, "tvos"))
    files = {
        "pubspec.yaml": GOOD_PUBSPEC.format(name=name),
        "README.md": "# widget_tvos\n",
        "CHANGELOG.md": "## 0.0.1\n\n* Initial.\n",
        "LICENSE": "BSD-3-Clause\n",
        f"tvos/{name}.podspec": "Pod::Spec.new do |s|\n  s.version = '0.0.1'\nend\n",
    }
    # `//README` addresses the *root* README, not a file inside the package —
    # keep it out of the per-package writes below.
    readme_override = overrides.pop("//README", None)
    files.update(overrides)
    for rel, content in files.items():
        if content is None:
            continue
        path = os.path.join(d, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
    readme = readme_override or (
        f"# Plugins\n\n## List of plugins\n\n| Plugin | Upstream |\n"
        f"|---|---|\n| [`{name}`](packages/{name}) | upstream |\n"
    )
    with open(os.path.join(root, "README.md"), "w", encoding="utf-8") as handle:
        handle.write(readme)
    return d


CASES = [
    ("baseline passes", {}, None),
    ("R1 prose mention is not a table row",
     {"//README": "# Plugins\n\nSee [the notes](packages/widget_tvos) if curious.\n"}, "R1"),
    ("R2 podspec drift",
     {"tvos/widget_tvos.podspec": "Pod::Spec.new do |s|\n  s.version = '0.0.2'\nend\n"}, "R2"),
    ("R2 commented-out s.version does not count",
     {"tvos/widget_tvos.podspec":
      "Pod::Spec.new do |s|\n  # s.version = '0.0.1'\n  s.version = '9.9.9'\nend\n"}, "R2"),
    ("R2 non-version changelog heading on top",
     {"CHANGELOG.md": "## Unreleased\n\n* wip\n\n## 0.0.1\n\n* Initial.\n"}, "R2"),
    ("R2 version with build metadata is compared verbatim",
     {"pubspec.yaml": GOOD_PUBSPEC.format(name="widget_tvos").replace(
         "version: 0.0.1", "version: 0.0.1+1")}, "R2"),
    ("R3 missing podspec is reported even without a version",
     {"pubspec.yaml": "name: widget_tvos\nflutter:\n  plugin:\n    platforms:\n"
                      "      tvos:\n        pluginClass: GoodPlugin\n",
      "tvos/widget_tvos.podspec": None}, "R3"),
    ("R3 unparseable pubspec fails rather than vanishing",
     {"pubspec.yaml": "name: [unclosed\n"}, "R3"),
    ("R5 sibling platform's pluginClass does not satisfy tvos",
     {"pubspec.yaml": "name: widget_tvos\nversion: 0.0.1\nflutter:\n  plugin:\n"
                      "    platforms:\n      tvos:\n        sharedDarwinSource: true\n"
                      "      ios:\n        pluginClass: RealIosPlugin\n"}, "R5"),
]


def selftest():
    failures = 0
    for label, overrides, expect in CASES:
        root = tempfile.mkdtemp(prefix="check_repo_selftest.")
        try:
            podspec_removed = overrides.get("tvos/widget_tvos.podspec", "keep") is None
            _fixture(root, **{k: v for k, v in overrides.items() if v is not None})
            if podspec_removed:
                os.remove(os.path.join(root, "packages", "widget_tvos", "tvos",
                                       "widget_tvos.podspec"))
            found, _ = check(root)
            rules = {rule for rule, _, _, _ in found}
            if expect is None:
                ok = not found
                detail = "expected a clean run, got: " + "; ".join(
                    f"{r} {m}" for r, _, m, _ in found)
            else:
                ok = expect in rules
                detail = f"expected {expect}, got {sorted(rules) or 'nothing'}"
            print(f"  {'ok  ' if ok else 'FAIL'}  {label}")
            if not ok:
                print(f"        {detail}")
                failures += 1
        finally:
            shutil.rmtree(root, ignore_errors=True)

    # Extra R4 cases: the shapes a substring test accepts while the override
    # still ships. Built directly, since they need an example/ subtree.
    for label, pubignore, expect_fail in [
        ("R4 real entry passes", "pubspec_overrides.yaml\n", False),
        ("R4 comment does not count", "# pubspec_overrides.yaml\n", True),
        ("R4 negation does not count", "!pubspec_overrides.yaml\n", True),
        ("R4 missing .pubignore", None, True),
    ]:
        root = tempfile.mkdtemp(prefix="check_repo_selftest.")
        try:
            d = _fixture(root)
            os.makedirs(os.path.join(d, "example"))
            open(os.path.join(d, "example", "pubspec_overrides.yaml"), "w").close()
            if pubignore is not None:
                with open(os.path.join(d, ".pubignore"), "w", encoding="utf-8") as handle:
                    handle.write(pubignore)
            found, _ = check(root)
            fired = "R4" in {rule for rule, _, _, _ in found}
            ok = fired == expect_fail
            print(f"  {'ok  ' if ok else 'FAIL'}  {label}")
            if not ok:
                print(f"        expected R4 to {'fire' if expect_fail else 'stay quiet'}")
                failures += 1
        finally:
            shutil.rmtree(root, ignore_errors=True)

    print()
    if failures:
        print(f"{failures} self-test case(s) failed — the gate itself is broken.")
        return 1
    print("Self-test passed: every rule fires on a bad tree and stays quiet on a good one.")
    return 0


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    positional = [a for a in args if not a.startswith("--")]
    root = os.path.abspath(positional[0] if positional else ".")
    if "--list" in args:
        for pkg in discover(os.path.join(root, "packages")):
            print(pkg)
        return 0
    return report(root)


if __name__ == "__main__":
    sys.exit(main())
