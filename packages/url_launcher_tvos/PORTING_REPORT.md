# url_launcher_tvos — porting report

Ported by `flutter-tvos plugin port`, then finished + verified by hand.

Source: `url_launcher_ios` 6.4.1 (Swift, Pigeon 26). Base platform: ios.
Output: `./url_launcher_tvos`

## Summary

| Status                                         | Count                                                                                         |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Pigeon methods kept + registered on tvOS       | 4 (`canLaunchUrl`, `launchUrl`, `openUrlInSafariViewController`, `closeSafariViewController`) |
| Native methods behaving as-is on tvOS          | 2 (`canLaunchUrl`, `launchUrl`)                                                               |
| Native methods returning an honest tvOS result | 2 (`openUrlInSafariViewController` → `.noUI`; `closeSafariViewController` → no-op)            |
| Native regions disabled on tvOS                | 1 (the entire `URLLaunchSession` — SFSafariViewController)                                    |
| tvOS build outlook                             | ✅ compiles (arm64 simulator, verified)                                                       |

## The one tvOS-absent API

`url_launcher_ios`'s only tvOS-incompatible surface is the **in-app browser**:
`SFSafariViewController` from **SafariServices**, which does not exist on tvOS.
Everything else — `UIApplication.canOpenURL` / `open(_:options:)` — is available
on tvOS. So `canLaunchUrl` and external `launchUrl` port unchanged; only the
in-app browser path is disabled.

## Native changes

- **`messages.g.swift` (generated Pigeon) — kept verbatim** except one line: the
  import gate widened from `#if os(iOS)` to `#if os(iOS) || os(tvOS)`. The porter
  had additionally wrapped `UrlLauncherApiSetup.setUp` in `#if !os(tvOS)` (it
  matched the string `SFSafariViewController` inside a doc comment) — that would
  have compiled out **all** channel registration on tvOS, so every method would
  throw `MissingPluginException`. Reverted to upstream so all four channels
  register.
- **`URLLaunchSession.swift`** — the whole class (`SFSafariViewControllerDelegate`
    - `import SafariServices`) is wrapped in `#if !os(tvOS)`; it is never referenced
      on tvOS.
- **`URLLauncherPlugin.swift`** — all four `UrlLauncherApi` methods are
  implemented (protocol conformance intact). `canLaunchUrl` / `launchUrl` are
  verbatim upstream. On tvOS, `openUrlInSafariViewController` returns
  `InAppLoadResult.noUI` (there is no browser UI to present) and
  `closeSafariViewController` is a no-op; the real Safari path stays under
  `#if !os(tvOS)`.
- **`ViewPresenter.swift`, `Launcher.swift`** — verbatim upstream; both are pure
  UIKit / `UIApplication` and compile on tvOS unchanged.

## Dart changes

This package's Dart runs **only on tvOS**, so it states tvOS behaviour directly
(no platform guards). The class is renamed `UrlLauncherIOS` → `UrlLauncherTvos`
(the `dartPluginClass` follows). The Pigeon-generated `messages.g.dart` is kept
**byte-identical to upstream 6.4.1**. Three capability points were made
tvOS-honest:

- `supportsMode(inAppBrowserView` / `inAppWebView)` → `false` (was `true`).
- `supportsCloseForMode(...)` → `false` (nothing to close).
- `launchUrl` with `platformDefault` resolves to an **external** launch
  (upstream opens web URLs in-app here).

## Packaging

- Podspec: no Flutter CocoaPod dependency (resolved via `FRAMEWORK_SEARCH_PATHS`);
  `s.platform = :tvos, '13.0'` (mirrors upstream's iOS 13 floor); privacy manifest
  shipped as a `resource_bundles` entry.
- Ships **both** a podspec (CocoaPods) and `tvos/Package.swift` (Swift Package
  Manager — the Flutter 3.44 default), matching the repo's other pure-Swift
  method-channel `_tvos` plugins (e.g. `shared_preferences_tvos`). flutter-tvos's
  Podfile skips SPM-owned plugins, so the two never double-link.
- **Version floor:** the package keeps the repo-standard `flutter: >=3.13.0`, not
  upstream 6.4.1's `>=3.38.0`. That bump was made upstream for iOS `UIScene`
  reasons in the in-app-browser presentation path — code this port disables on
  tvOS — so the shipped tvOS slice needs nothing newer, and this stays consistent
  with the sibling `_tvos` packages.

## Verification

- `dart analyze` — no issues. `flutter test` — 4/4 pass (registration + the
  tvOS `supportsMode` behaviour).
- **`flutter-tvos build tvos --simulator --debug`** from `example/` — **Xcode
  build succeeds (arm64)**.
- **Runtime on a booted Apple TV 4K simulator** — all four Pigeon channels were
  exercised; every one round-trips with **no `MissingPluginException`**:
    - `canLaunchUrl(https://flutter.dev)` → `true`
    - `launchUrl(external)` → `false` (nothing on the sim handles a bare web URL)
    - in-app path → `PlatformException(no_ui_available)` (the honest tvOS stub)
    - `closeWebView()` → returns (no-op)
    - `supportsMode`: `inAppBrowserView=false`, `externalApplication=true`

    Note: tvOS `canLaunchUrl` returned `true` for the web URL even though
    `launchUrl` then returned `false` — so `canLaunchUrl` is not a reliable gate on
    tvOS; callers should use the `launchUrl` return value (documented in the
    README).

- **Real external launch** — the example registers its own `ullauncherdemo://`
  URL scheme (`CFBundleURLTypes` + `LSApplicationQueriesSchemes`) and launches it.
  On the sim: `canLaunchUrl=true`, **`launchUrl(external)=true`**, and the native
  `AppDelegate.application(_:open:)` logs the delivered URL — i.e.
  `UIApplication.open` genuinely hands off on tvOS. This is the same mechanism an
  app deep link (`imdb://`, etc.) uses; a bare web URL fails only because no app
  claims it (no browser).
- **Cross-app launch (separate manual checks — the targets below are _not_ part
  of the shipped package).** To confirm `launchUrl` opens a _different_ app, not
  just the example itself: on the **simulator**, a throwaway second app
  registering `targetapp://` was installed and the example (temporarily pointed at
  it) launched it — the second app's `AppDelegate` logged the delivered URL. On a
  **physical Apple TV 4K** (release/AOT, `devicectl` install), the example
  (temporarily pointed at an App Store URL) called `launchUrl` and the **App
  Store** opened. Both confirm genuine app-to-app hand-off on real tvOS hardware.
  The shipped example itself only launches its own `ullauncherdemo://` scheme
  (above), so it stays self-contained.

## Checklist

- [x] All Pigeon methods kept and registered on tvOS (no `MissingPluginException`).
- [x] tvOS-absent API (`SFSafariViewController`) disabled behind `#if !os(tvOS)`;
      the two affected handlers return an honest result rather than crashing.
- [x] Generated files (`messages.g.dart`, `messages.g.swift`) match upstream
      (the Swift file differs only by the import gate).
- [x] `flutter-tvos build tvos --simulator` compiles the example.
- [x] Version set (`0.0.1`) and `CHANGELOG.md` updated.
