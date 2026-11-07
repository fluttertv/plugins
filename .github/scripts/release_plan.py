#!/usr/bin/env python3
"""Decide which packages on this commit need publishing to pub.dev.

A package is a release candidate when its pubspec.yaml version is not on
pub.dev yet. That is the question that matters, rather than "did pubspec.yaml
change in this push": it is the same answer for a squash merge, a merge commit
or a stack of pushes, and a release whose publish failed is picked up again by
the next run instead of being lost with the diff that introduced it.

For each candidate the version must also be:
  - the newest `## ` heading of CHANGELOG.md (an unreleased or missing entry
    blocks the release), and
  - newer than every version already on pub.dev (publishing an older version
    is legal on pub.dev, but never what a merge to main means here — do it by
    hand if you really need it).

A package that is not on pub.dev at all is skipped with a warning: pub.dev
only allows automated publishing for packages that already exist, so the
first version has to go up with `flutter pub publish` by hand.

Output: a JSON list on stdout, one {package, version, tag, tag_exists} per
candidate. `tag_exists` means an earlier run tagged this version but pub.dev
still does not have it — the publish failed or was never approved — and the
release job re-dispatches publishing instead of tagging again.

Exits non-zero if any package's metadata is inconsistent, so a bad bump fails
the run in plain sight rather than quietly not publishing. With
--github-output it exits 0 and writes `problems=<n>` instead, so one bad bump
does not hold back the other packages released in the same merge; the
workflow fails the run on that count once they are out.

Usage:
    release_plan.py <repo-root> [--github-output]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_repo import (  # noqa: E402
    discover, load_yaml, newest_changelog_version, read_text,
)

SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+[0-9A-Za-z.-]+)?$")


def tag_for(package, version):
    """Must match the tag pattern configured on pub.dev: <package>-v{{version}}."""
    return f"{package}-v{version}"


def semver_key(version):
    """Sort key with semver precedence: a prerelease sorts below its release."""
    m = SEMVER.match(version)
    if not m:
        return None
    major, minor, patch, pre = m.groups()
    pre_key = (1,) if pre is None else (0, *[
        (0, int(p), "") if p.isdigit() else (1, 0, p) for p in pre.split(".")
    ])
    return (int(major), int(minor), int(patch), pre_key)


def pub_versions(package):
    """Published versions, [] if the package does not exist, None on error."""
    url = f"https://pub.dev/api/packages/{package}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.pub.v2+json",
        "User-Agent": "fluttertv-plugins-release-plan",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return []
        print(f"error: {url}: HTTP {exc.code}", file=sys.stderr)
        return None
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"error: {url}: {exc}", file=sys.stderr)
        return None
    return [v["version"] for v in data.get("versions", [])]


def remote_tags(root):
    """Tag names on origin. ls-remote, not local tags: the checkout is shallow
    and may not have fetched them."""
    proc = subprocess.run(["git", "ls-remote", "--tags", "origin"], cwd=root,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"git ls-remote failed: {proc.stderr.strip()}")
    tags = set()
    for line in proc.stdout.splitlines():
        ref = line.split("\t")[-1]
        if ref.startswith("refs/tags/"):
            tags.add(ref[len("refs/tags/"):].removesuffix("^{}"))
    return tags


def plan(root, tags):
    candidates, problems = [], []
    for pkg in discover(os.path.join(root, "packages")):
        d = os.path.join(root, "packages", pkg)
        pubspec, err = load_yaml(os.path.join(d, "pubspec.yaml"))
        if err or not isinstance(pubspec, dict):
            problems.append(f"{pkg}: pubspec.yaml unreadable ({err})")
            continue
        if pubspec.get("publish_to") == "none":
            continue
        name, version = pubspec.get("name"), pubspec.get("version")
        if name != pkg:
            problems.append(f"{pkg}: pubspec name is '{name}', not the directory name")
            continue
        if not version or semver_key(version) is None:
            problems.append(f"{pkg}: version '{version}' is not semver")
            continue

        published = pub_versions(pkg)
        if published is None:
            problems.append(f"{pkg}: could not read pub.dev — not deciding blind")
            continue
        if version in published:
            continue
        if not published:
            print(f"::warning::{pkg} is not on pub.dev. Automated publishing only "
                  f"works for existing packages — publish {version} by hand once.",
                  file=sys.stderr)
            continue

        newest = max((v for v in published if semver_key(v)), key=semver_key, default=None)
        if newest and semver_key(version) <= semver_key(newest):
            problems.append(f"{pkg}: {version} is not newer than {newest} on pub.dev")
            continue
        text, err = read_text(os.path.join(d, "CHANGELOG.md"))
        top, heading = newest_changelog_version(text) if text is not None else (None, None)
        if top != version:
            problems.append(f"{pkg}: version {version} but the newest CHANGELOG "
                            f"heading is '{heading}' — add a '## {version}' entry")
            continue
        tag = tag_for(pkg, version)
        candidates.append({"package": pkg, "version": version, "tag": tag,
                           "tag_exists": tag in tags})
    return candidates, problems


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--github-output", action="store_true",
                        help="also write candidates=<json> to $GITHUB_OUTPUT")
    opts = parser.parse_args()
    root = os.path.abspath(opts.root)
    candidates, problems = plan(root, remote_tags(root))
    for p in problems:
        print(f"::error::{p}", file=sys.stderr)
    for c in candidates:
        note = " (tag exists; re-dispatching publish)" if c["tag_exists"] else ""
        print(f"release: {c['package']} {c['version']} as {c['tag']}{note}",
              file=sys.stderr)
    if not candidates:
        print("Nothing to release: every package's version is already on pub.dev.",
              file=sys.stderr)
    payload = json.dumps(candidates)
    print(payload)
    if opts.github_output:
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
            fh.write(f"candidates={payload}\n")
            fh.write(f"problems={len(problems)}\n")
        # In Actions the problems surface through their own job, so the
        # healthy candidates on this commit still get released.
        return 0
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
