## What does this PR do?

<!-- A clear description of the change and the motivation behind it.
     Link related issues: "Fixes #123" / "Part of #123". -->

**Package(s) touched:** <!-- e.g. sqflite_tvos, path_provider_tvos -->

## How was it tested?

<!-- tvOS behaviour frequently differs between the simulator and real hardware:
     the simulator's sandbox is more permissive, and it renders on the host Mac
     GPU. A change that works in the simulator can still fail on an Apple TV.
     Say which you used, and give versions/model where relevant. -->

- [ ] Ran the package's `example/` app
- [ ] Verified on tvOS **simulator** (version: ___)
- [ ] Verified on a **physical Apple TV** (model / tvOS version: ___)
- [ ] `dart analyze` is clean for the package

## Versioning & changelog

<!-- Every package here is published to pub.dev under the fluttertv.dev
     publisher and versioned independently. A user-visible change that doesn't
     bump the version cannot reach anyone. -->

- [ ] Bumped `version:` in the package's `pubspec.yaml` (or: no user-visible change — explain below)
- [ ] Added a matching entry at the top of the package's `CHANGELOG.md`, under a heading identical to the new version
- [ ] The entry calls out any **behaviour change** — a changed default path, a changed return value, anything that silently alters what an existing app sees
- [ ] Version choice follows semver for `0.x`: bug fix → patch (`0.0.1` → `0.0.2`); new API or breaking change → minor (`0.0.x` → `0.1.0`)

## Checklist

- [ ] Only the intended package's files are touched (this is a monorepo — unrelated packages should not appear in the diff)
- [ ] No secrets, absolute local paths, or `TODO`/debug leftovers in the diff
- [ ] If the change reflects a tvOS platform constraint (sandbox, focus engine, missing framework), the package `README.md` "Limitations / differs from iOS" section is updated to match
- [ ] If the same constraint affects sibling packages, they're noted below rather than fixed here

## Notes for reviewers

<!-- Trade-offs, follow-ups, anything you're unsure about, or sibling packages
     that likely need the same treatment. -->

---

<sub>Maintainers: publishing to pub.dev is irreversible — a version number can never be reused. Run `dart pub publish --dry-run` and check the package's current `latest` on pub.dev before publishing.</sub>
