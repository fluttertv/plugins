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

import argparse
import fnmatch
import os
import re
import shutil
import sys
import tempfile

import yaml

REQUIRED_FILES = ["pubspec.yaml", "README.md", "CHANGELOG.md", "LICENSE"]


def load_yaml(path):
    """(parsed, error). `error` is None when the file parsed, even to nothing.

    BaseLoader rather than safe_load, so every scalar stays a string. safe_load
    types `version: 1.10` as the float 1.1, and this checker compares versions
    as text — it would have reported "podspec says 1.10, pubspec.yaml says 1.1"
    about a tree where all three files literally agree.
    """
    try:
        with open(path, encoding="utf-8") as handle:
            return yaml.load(handle, Loader=yaml.BaseLoader), None
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
    platform's class. The shape that slipped through was a `tvos:` block present
    but pluginClass-less, followed by a platform that had one — a package with
    no `tvos:` block at all was still caught. That is the case the R5 self-test
    now pins, and the rule whose failure is invisible until an app calls it.
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
        # Tolerate `./packages/x`, a trailing slash, an `#anchor` and a link
        # title — all legitimate rows that the stricter form rejected.
        rows.update(re.findall(r"\(\.?/?packages/([A-Za-z0-9_]+)[/#)\s]", line))
    return rows


def pubignore_excludes(text, relpath):
    """True if `relpath` (relative to the package root) is excluded.

    Gitignore semantics, and the parts that matter here are the ones that are
    easy to get wrong:

    * **Last match wins.** A `!pattern` after a matching pattern re-includes the
      file. Skipping `!` lines instead — which an earlier version did — means a
      negation can never take effect, and `foo` followed by `!foo` reads as
      excluded when the file actually ships.
    * **Match the path, not the name.** `other_dir/pubspec_overrides.yaml`
      excludes a file in `other_dir/`, and says nothing about the one in
      `example/`. Comparing basenames accepted it anyway — the same shape of
      sloppiness as the substring test this rule started with.
    * A pattern with no slash matches at any depth; one with a slash is
      anchored to the package root.
    """
    excluded = False
    for raw in text.split("\n"):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        negated = line.startswith("!")
        if negated:
            line = line[1:].strip()
        pattern = line.rstrip("/")
        if not pattern:
            continue
        if pattern.startswith("/") or "/" in pattern:
            # Anchored to the package root. Excluding a *directory* excludes its
            # whole subtree, so match the pattern against every leading prefix
            # of the path, not only against the path itself — `/example/` and
            # `/example` both cover `example/pubspec_overrides.yaml`, which is
            # what `git check-ignore` says and what pub follows. Comparing only
            # the full path called that a miss and produced a false R4 telling
            # the author to add an entry they had effectively already written.
            anchored = pattern.lstrip("/")
            parts = relpath.split("/")
            prefixes = ["/".join(parts[:i]) for i in range(1, len(parts) + 1)]
            hit = any(fnmatch.fnmatch(prefix, anchored) for prefix in prefixes)
        else:
            # Unanchored: matches the basename, or any directory component.
            parts = relpath.split("/")
            hit = any(fnmatch.fnmatch(part, pattern) for part in parts)
        if hit:
            excluded = not negated
    return excluded


def newest_changelog_version(text):
    """The first `## ` heading's version, or (None, heading).

    The first heading of any kind, not the first numeric one: matching on a
    leading digit skipped `## Unreleased` and validated the released entry
    underneath it, so a changelog whose top section had no version passed.
    """
    # Strip fenced blocks first: a ``` example containing `## 0.0.1` above the
    # real `## Unreleased` heading would otherwise be read as the newest entry,
    # which is the original defect through a different door.
    stripped = re.sub(r"^```.*?^```", "", text, flags=re.M | re.S)
    match = re.search(r"^##\s+(.+?)\s*$", stripped, re.M)
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

        # Only the version comparisons and R5 need the pubspec. The podspec,
        # changelog and override rules do not — and an earlier revision's
        # `continue` here cancelled all of them on any parse error, reporting
        # one problem out of five and saying nothing about the four it skipped.
        # That is the same mistake the podspec check's comment below records
        # having already learned once.
        pubspec_path = os.path.join(d, "pubspec.yaml")
        pubspec, err = load_yaml(pubspec_path)
        if err is not None:
            fail("R3", pkg, f"pubspec.yaml could not be parsed ({err})",
                 "R2's version comparison and R5 are skipped for this package")
            pubspec = None
        elif pubspec is None:
            fail("R3", pkg, "pubspec.yaml is empty",
                 "R2's version comparison and R5 are skipped for this package")
        elif not isinstance(pubspec, dict):
            fail("R3", pkg, "pubspec.yaml is not a YAML mapping",
                 "R2's version comparison and R5 are skipped for this package")
            pubspec = None

        version = None
        if isinstance(pubspec, dict):
            raw_version = pubspec.get("version")
            version = str(raw_version).strip() if raw_version is not None else None
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
            else:
                # Dart allows `0.0.1+1`; CocoaPods does not. Pod::Version derives
                # from Gem::Version, which rejects `+` outright, so demanding the
                # podspec repeat the build metadata would leave an author with a
                # red gate or a podspec that raises. Compare the release part.
                want = version.split("+")[0] if version else None
                if want and declared != want:
                    fail("R2", pkg, f"{spec} says {declared}, pubspec.yaml says {version}",
                         f"set s.version = '{want}'"
                         + (" (CocoaPods rejects Dart's `+build` suffix)"
                            if want != version else ""))

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

        # R4 — a nested override must not reach the archive. Walked rather
        # than stat-ing example/ alone: the override only has to be below the
        # package root to ship, and an example restructured into a subdirectory
        # would otherwise become invisible to this rule.
        nested = [
            os.path.relpath(os.path.join(where, "pubspec_overrides.yaml"), d)
            for where, _, files in os.walk(d)
            if "pubspec_overrides.yaml" in files and os.path.abspath(where) != os.path.abspath(d)
        ]
        if nested:
            pubignore_path = os.path.join(d, ".pubignore")
            pubignore, pubignore_err = read_text(pubignore_path)
            if pubignore is not None:
                covered = all(pubignore_excludes(pubignore, rel) for rel in nested)
            else:
                covered = False
                if os.path.exists(pubignore_path):
                    # Blaming the override would send the reader to the wrong
                    # file; the override is fine, the .pubignore is unreadable.
                    fail("R3", pkg, f".pubignore is unreadable ({pubignore_err})")
            if not covered:
                fail("R4", pkg,
                     f"{', '.join(sorted(nested))} is committed but not excluded by .pubignore",
                     "add `pubspec_overrides.yaml` to .pubignore, or delete the "
                     "override if the dependency it pins is now published")

        # R5 — the tvOS plugin class. Skipped (loudly, above) when the pubspec
        # did not parse; a missing class cannot be distinguished from a missing
        # file, and guessing either way would be a verdict we cannot support.
        if pubspec is None:
            pass
        elif not tvos_plugin_class(pubspec):
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
    # `0.0.1+1` in the pubspec against `0.0.1` in the podspec is CORRECT, since
    # CocoaPods cannot express the build metadata. This case asserts the rule
    # stays quiet — an earlier revision asserted the opposite and would have
    # forced a podspec version that raises.
    ("R2 build metadata is stripped, not demanded of the podspec",
     {"pubspec.yaml": GOOD_PUBSPEC.format(name="widget_tvos").replace(
         "version: 0.0.1", "version: 0.0.1+1"),
      "CHANGELOG.md": "## 0.0.1+1\n\n* Initial.\n"}, None),
    # Expects BOTH rules: the point of the case is that R3 still runs when R2
    # has already failed, so asserting only R3 would let the co-firing it
    # demonstrates go unchecked.
    ("R3 missing podspec is reported even without a version",
     {"pubspec.yaml": "name: widget_tvos\nflutter:\n  plugin:\n    platforms:\n"
                      "      tvos:\n        pluginClass: GoodPlugin\n",
      "tvos/widget_tvos.podspec": None}, ["R2", "R3"]),
    ("R3 unparseable pubspec fails rather than vanishing",
     {"pubspec.yaml": "name: [unclosed\n"}, "R3"),
    ("R3 each required file is enforced — LICENSE", {"LICENSE": None}, "R3"),
    ("R3 each required file is enforced — CHANGELOG", {"CHANGELOG.md": None}, "R3"),
    ("R3 each required file is enforced — README", {"README.md": None}, "R3"),
    ("R2 podspec without an s.version at all",
     {"tvos/widget_tvos.podspec": "Pod::Spec.new do |s|\n  s.name = 'x'\nend\n"}, "R2"),
    ("R2 changelog with no ## heading", {"CHANGELOG.md": "Nothing yet.\n"}, "R2"),
    ("R2 changelog heading inside a fence is not the newest",
     {"CHANGELOG.md": "```\n## 0.0.1\n```\n\n## Unreleased\n\n* wip\n"}, "R2"),
    ("R5 no flutter block at all",
     {"pubspec.yaml": "name: widget_tvos\nversion: 0.0.1\n"}, "R5"),
    ("R5 platforms without a tvos key",
     {"pubspec.yaml": "name: widget_tvos\nversion: 0.0.1\nflutter:\n  plugin:\n"
                      "    platforms:\n      ios:\n        pluginClass: RealIosPlugin\n"}, "R5"),
    ("R5 sibling platform's pluginClass does not satisfy tvos",
     {"pubspec.yaml": "name: widget_tvos\nversion: 0.0.1\nflutter:\n  plugin:\n"
                      "    platforms:\n      tvos:\n        sharedDarwinSource: true\n"
                      "      ios:\n        pluginClass: RealIosPlugin\n"}, "R5"),
]


def selftest():
    failures = 0
    exercised = set()
    for label, overrides, expect in CASES:
        root = tempfile.mkdtemp(prefix="check_repo_selftest.")
        try:
            # `None` means "this file should not exist" — handled inside
            # _fixture for every path. Filtering it out here instead left that
            # branch dead and the deletion hardcoded to one filename, so a new
            # case like {"LICENSE": None} silently built a *good* tree.
            _fixture(root, **dict(overrides))
            found, _ = check(root)
            rules = sorted({rule for rule, _, _, _ in found})
            exercised.update(rules)
            if expect is None:
                ok = not found
                detail = "expected a clean run, got: " + "; ".join(
                    f"{r} {m}" for r, _, m, _ in found)
            else:
                # Exact set, not membership. `expect in rules` passed when the
                # expected rule fired from a *different* branch than the case
                # was written for — deleting R2's "heading is not a version"
                # arm still produced an R2, from the version-mismatch arm, and
                # the case stayed green over a dead branch.
                ok = rules == sorted(set(expect if isinstance(expect, list) else [expect]))
                detail = f"expected exactly {expect}, got {rules or 'nothing'}"
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
        ("R4 root-anchored entry does not cover example/",
         "/pubspec_overrides.yaml\n", True),
        ("R4 a different filename does not count",
         "my_pubspec_overrides.yaml\n", True),
        ("R4 an entry scoped to another directory does not count",
         "other_dir/pubspec_overrides.yaml\n", True),
        ("R4 negation after a match re-includes the file",
         "pubspec_overrides.yaml\n!example/pubspec_overrides.yaml\n", True),
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
            exercised.update(rule for rule, _, _, _ in found)
            fired = "R4" in {rule for rule, _, _, _ in found}
            ok = fired == expect_fail
            print(f"  {'ok  ' if ok else 'FAIL'}  {label}")
            if not ok:
                print(f"        expected R4 to {'fire' if expect_fail else 'stay quiet'}")
                failures += 1
        finally:
            shutil.rmtree(root, ignore_errors=True)

    # R0 — the guards against a vacuous run. Built directly: both need a tree
    # with no valid package in it, which _fixture exists to prevent.
    for label, build, expect_rule in [
        ("R0 empty packages/ is not a silent pass",
         lambda root: os.makedirs(os.path.join(root, "packages")), "R0"),
        # Pins the regression `discover`'s docstring records: enumerating by
        # "directories containing a pubspec" made such a directory VANISH from
        # the run instead of failing it, and silently disagreed with the
        # workflow's matrix. Nothing caught that until it was found by hand.
        ("R3 a package directory with no pubspec is reported, not skipped",
         lambda root: (_fixture(root),
                       os.makedirs(os.path.join(root, "packages", "stray_tvos"))), "R3"),
        ("R0 unreadable root README is fatal, not skipped",
         lambda root: (_fixture(root), os.remove(os.path.join(root, "README.md"))), "R0"),
    ]:
        root = tempfile.mkdtemp(prefix="check_repo_selftest.")
        try:
            build(root)
            found, _ = check(root)
            rules = {rule for rule, _, _, _ in found}
            exercised.update(rules)
            ok = expect_rule in rules
            print(f"  {'ok  ' if ok else 'FAIL'}  {label}")
            if not ok:
                print(f"        expected {expect_rule}, got {sorted(rules) or 'nothing'}")
                failures += 1
        finally:
            shutil.rmtree(root, ignore_errors=True)

    # The self-test is what certifies every rule, so it must not be able to
    # certify nothing. Emptying CASES made an earlier revision print "passed"
    # and exit 0 with zero assertions — the exact anti-pattern this file exists
    # to catch, one level up. Assert coverage of the rule set explicitly.
    expected_rules = {"R0", "R1", "R2", "R3", "R4", "R5"}
    missing = expected_rules - exercised
    if missing:
        print(f"  FAIL  no case exercises {', '.join(sorted(missing))}")
        print("        A rule with no case is indistinguishable from a broken one.")
        failures += 1

    print()
    if failures:
        print(f"{failures} self-test problem(s) — the gate itself is not trustworthy.")
        return 1
    print(f"Self-test passed: {len(CASES) + 11} cases, every rule in "
          f"{', '.join(sorted(expected_rules))} both fires and stays quiet.")
    return 0


def main():
    # argparse rather than scanning sys.argv: the hand-rolled version accepted
    # `check_repo.py <root> --selftest`, ran the self-test, ignored the root and
    # exited 0 — so collapsing the two CI steps into one command would have made
    # the structural gate permanently green. It also silently accepted `--slftest`
    # as "no flags at all".
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--list", action="store_true",
                      help="print package names, one per line")
    mode.add_argument("--selftest", action="store_true",
                      help="verify every rule fires, and does not")
    opts = parser.parse_args()

    if opts.selftest:
        if opts.root != ".":
            parser.error("--selftest takes no root; it builds its own trees")
        return selftest()
    root = os.path.abspath(opts.root)
    if opts.list:
        for pkg in discover(os.path.join(root, "packages")):
            print(pkg)
        return 0
    return report(root)


if __name__ == "__main__":
    sys.exit(main())
