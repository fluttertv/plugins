#!/usr/bin/env python3
"""Structural checks over packages/ that need neither Flutter nor a network.

These are the invariants nobody re-reads a checklist for. Each one has been
broken at least once, or was caught only because a human happened to look:

  R1  every package has a row in the root README's Ports table
      Missed on the firebase_performance_tvos port (#9). AUTHORING.md makes it
      step 4, and the package is otherwise undiscoverable from the repo index.

  R2  pubspec version == podspec s.version == the top CHANGELOG heading
      path_provider_tvos and sqflite_tvos had already drifted. The podspec
      version is inert while pods resolve by :path, so nothing surfaces it.

  R3  the files a published package cannot ship without

  R4  a committed pubspec_overrides.yaml is excluded from the published archive
      A local path override that reaches pub.dev makes the package uninstallable.

  R5  the tvOS plugin class is declared
      Without flutter.plugin.platforms.tvos.pluginClass the CLI never registers
      the plugin and the app gets MissingPluginException at the first call —
      at runtime, on a device, with nothing pointing at the cause.

Usage: check_repo.py [repo-root]
Exits non-zero if any check fails.
"""

import os
import re
import sys

REQUIRED_FILES = ["pubspec.yaml", "README.md", "CHANGELOG.md", "LICENSE"]


def scalar(text, key):
    """Top-level `key: value` from a pubspec, without a YAML dependency."""
    m = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.M)
    return m.group(1).strip().strip("\"'") if m else None


def tvos_plugin_class(text):
    """flutter.plugin.platforms.tvos.pluginClass, by indentation."""
    m = re.search(r"^\s*tvos:\s*$", text, re.M)
    if not m:
        return None
    rest = text[m.end():]
    for line in rest.split("\n"):
        if line.strip() and not line.startswith((" ", "\t")):
            break  # dedented out of the tvos: block
        m2 = re.match(r"\s*pluginClass:\s*(\S+)", line)
        if m2:
            return m2.group(1)
    return None


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    pkg_root = os.path.join(root, "packages")
    if not os.path.isdir(pkg_root):
        print(f"ERROR: no packages/ under {root}")
        return 1

    try:
        readme = open(os.path.join(root, "README.md"), encoding="utf-8").read()
    except OSError as exc:
        print(f"ERROR: cannot read the root README ({exc})")
        return 1

    packages = sorted(
        d for d in os.listdir(pkg_root)
        if os.path.isfile(os.path.join(pkg_root, d, "pubspec.yaml"))
    )
    if not packages:
        print("ERROR: packages/ holds no package with a pubspec.yaml")
        return 1

    failures = []

    def fail(pkg, rule, msg, fix=None):
        failures.append((pkg, rule, msg, fix))

    for pkg in packages:
        d = os.path.join(pkg_root, pkg)

        # R3 — required files
        for name in REQUIRED_FILES:
            if not os.path.isfile(os.path.join(d, name)):
                fail(pkg, "R3", f"{name} is missing")

        pubspec_path = os.path.join(d, "pubspec.yaml")
        pubspec = open(pubspec_path, encoding="utf-8").read()

        # R1 — README Ports row
        if f"packages/{pkg})" not in readme:
            fail(pkg, "R1", "no row in the root README's Ports table",
                 f"add a row linking packages/{pkg} — AUTHORING.md step 4")

        # R2 — three versions agree
        version = scalar(pubspec, "version")
        if not version:
            fail(pkg, "R2", "pubspec.yaml declares no version")
        else:
            podspecs = []
            tvos_dir = os.path.join(d, "tvos")
            if os.path.isdir(tvos_dir):
                podspecs = [f for f in os.listdir(tvos_dir) if f.endswith(".podspec")]
            if not podspecs:
                fail(pkg, "R3", "tvos/ ships no .podspec")
            for spec in podspecs:
                text = open(os.path.join(tvos_dir, spec), encoding="utf-8").read()
                m = re.search(r"s\.version\s*=\s*['\"]([^'\"]+)['\"]", text)
                if not m:
                    fail(pkg, "R2", f"{spec} declares no s.version")
                elif m.group(1) != version:
                    fail(pkg, "R2",
                         f"{spec} says {m.group(1)}, pubspec.yaml says {version}",
                         f"set s.version = '{version}'")

            changelog_path = os.path.join(d, "CHANGELOG.md")
            if os.path.isfile(changelog_path):
                cl = open(changelog_path, encoding="utf-8").read()
                m = re.search(r"^##\s+\[?([0-9][^\]\s]*)\]?", cl, re.M)
                if not m:
                    fail(pkg, "R2", "CHANGELOG.md has no `## <version>` heading")
                elif m.group(1) != version:
                    fail(pkg, "R2",
                         f"CHANGELOG.md starts at {m.group(1)}, "
                         f"pubspec.yaml says {version}",
                         f"add a `## {version}` entry at the top")

        # R4 — a committed override must not reach the published archive
        if os.path.isfile(os.path.join(d, "pubspec_overrides.yaml")):
            pubignore = os.path.join(d, ".pubignore")
            listed = (
                os.path.isfile(pubignore)
                and "pubspec_overrides.yaml" in open(pubignore, encoding="utf-8").read()
            )
            if not listed:
                fail(pkg, "R4",
                     "pubspec_overrides.yaml is committed but not in .pubignore",
                     "add `pubspec_overrides.yaml` to .pubignore, or delete the "
                     "override if the dependency it pins is now published")

        # R5 — the tvOS plugin class
        if not tvos_plugin_class(pubspec):
            fail(pkg, "R5",
                 "pubspec.yaml declares no flutter.plugin.platforms.tvos.pluginClass",
                 "without it the CLI never registers the plugin — "
                 "MissingPluginException at the first call")

    print(f"Checked {len(packages)} package(s) under packages/\n")
    if not failures:
        print("  OK — README rows, versions, required files, "
              "overrides and tvOS plugin classes all consistent.")
        return 0

    width = max(len(p) for p, _, _, _ in failures)
    for pkg, rule, msg, fix in failures:
        print(f"  {rule}  {pkg.ljust(width)}  {msg}")
        if fix:
            print(f"      → {fix}")
    print(f"\n{len(failures)} problem(s). See the docstring in "
          f".github/scripts/check_repo.py for why each rule exists.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
