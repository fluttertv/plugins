# FlutterTV Plugins

Flutter plugins with **Apple TV (tvOS)** support, maintained by the
[fluttertv.dev](https://fluttertv.dev) organization.

These are companions to [flutter-tvos](https://github.com/fluttertv/flutter-tvos)
— the Flutter tvOS custom embedder. Most are federated `*_tvos`
implementations of popular pub.dev plugins, produced with the
`flutter-tvos plugin port` tool and finished/verified by hand.

> **Publishing status:** not yet on pub.dev — use the git dependencies
> shown under [Usage](#usage). The pub.dev badges below will resolve
> once published under the `fluttertv.dev` verified publisher.

## List of plugins

Every plugin below **builds for tvOS** (`flutter-tvos build tvos
--simulator --debug` is green). "Verified" shows how far it was
exercised: **sim** = tvOS simulator, **device** = a physical Apple TV.
Each package's `README.md` has the full ✅/⚠️/❌ API breakdown and its
`PORTING_REPORT.md` has the port detail + checklist.

| Plugin | Upstream | tvOS support | Verified |
|---|---|---|---|
| [`shared_preferences_tvos`](packages/shared_preferences_tvos) [![pub](https://img.shields.io/pub/v/shared_preferences_tvos.svg)](https://pub.dev/packages/shared_preferences_tvos) | [`shared_preferences`](https://pub.dev/packages/shared_preferences) | ✅ Full (`NSUserDefaults`) | sim + **device** 63/63 |
| [`video_player_tvos`](packages/video_player_tvos) [![pub](https://img.shields.io/pub/v/video_player_tvos.svg)](https://pub.dev/packages/video_player_tvos) | [`video_player`](https://pub.dev/packages/video_player) | ✅ Full — asset/network/file + texture | sim + **device** 14/14 |
| [`wakelock_plus_tvos`](packages/wakelock_plus_tvos) [![pub](https://img.shields.io/pub/v/wakelock_plus_tvos.svg)](https://pub.dev/packages/wakelock_plus_tvos) | [`wakelock_plus`](https://pub.dev/packages/wakelock_plus) | ✅ Full | sim + **device** 2/2 |
| [`connectivity_plus_tvos`](packages/connectivity_plus_tvos) [![pub](https://img.shields.io/pub/v/connectivity_plus_tvos.svg)](https://pub.dev/packages/connectivity_plus_tvos) | [`connectivity_plus`](https://pub.dev/packages/connectivity_plus) | ⚠️ Works; no cellular result | sim + **device** |
| [`path_provider_tvos`](packages/path_provider_tvos) [![pub](https://img.shields.io/pub/v/path_provider_tvos.svg)](https://pub.dev/packages/path_provider_tvos) | [`path_provider`](https://pub.dev/packages/path_provider) | ⚠️ Works; no Downloads/External | sim + **device** |
| [`flutter_secure_storage_tvos`](packages/flutter_secure_storage_tvos) [![pub](https://img.shields.io/pub/v/flutter_secure_storage_tvos.svg)](https://pub.dev/packages/flutter_secure_storage_tvos) | [`flutter_secure_storage`](https://pub.dev/packages/flutter_secure_storage) | ⚠️ Keychain works; no biometric gating | sim |
| [`device_info_plus_tvos`](packages/device_info_plus_tvos) [![pub](https://img.shields.io/pub/v/device_info_plus_tvos.svg)](https://pub.dev/packages/device_info_plus_tvos) | [`device_info_plus`](https://pub.dev/packages/device_info_plus) | ⚠️ Works; `isiOSAppOnMac/Vision` = false | sim |
| [`package_info_plus_tvos`](packages/package_info_plus_tvos) [![pub](https://img.shields.io/pub/v/package_info_plus_tvos.svg)](https://pub.dev/packages/package_info_plus_tvos) | [`package_info_plus`](https://pub.dev/packages/package_info_plus) | ⚠️ Works; `installerStore` = null | sim |
| [`audioplayers_tvos`](packages/audioplayers_tvos) [![pub](https://img.shields.io/pub/v/audioplayers_tvos.svg)](https://pub.dev/packages/audioplayers_tvos) | [`audioplayers`](https://pub.dev/packages/audioplayers) | ⚠️ Plays; audio-routing options no-op | sim |
| [`flutter_tts_tvos`](packages/flutter_tts_tvos) [![pub](https://img.shields.io/pub/v/flutter_tts_tvos.svg)](https://pub.dev/packages/flutter_tts_tvos) | [`flutter_tts`](https://pub.dev/packages/flutter_tts) | ⚠️ Speaks; audio-routing options no-op | sim |
| [`sqflite_tvos`](packages/sqflite_tvos) [![pub](https://img.shields.io/pub/v/sqflite_tvos.svg)](https://pub.dev/packages/sqflite_tvos) | [`sqflite`](https://pub.dev/packages/sqflite) | ✅ Full SQLite | sim |

### Evaluated but not provided

These were assessed and **deliberately not shipped** — their core
capability does not exist on tvOS, so a published package would be
misleading:

| Plugin | Why not on tvOS |
|---|---|
| [`url_launcher`](https://pub.dev/packages/url_launcher) | No Safari / arbitrary URL or app launching on tvOS |
| [`google_sign_in`](https://pub.dev/packages/google_sign_in) | No GoogleSignIn tvOS SDK; tvOS uses a different device-pairing flow |
| [`geolocator`](https://pub.dev/packages/geolocator) | No location services on Apple TV |
| [`permission_handler`](https://pub.dev/packages/permission_handler) | tvOS lacks the permission surfaces (location, camera, photos, …) |
| [`firebase_core`](https://pub.dev/packages/firebase_core) | No tvOS slice of the Firebase Apple SDK |
| [`in_app_purchase`](https://pub.dev/packages/in_app_purchase) | StoreKit2 port has an unresolved protocol-conformance cascade |
| [`network_info_plus`](https://pub.dev/packages/network_info_plus) | Wi‑Fi SSID/BSSID APIs do not exist on tvOS |
| [`webview_flutter`](https://pub.dev/packages/webview_flutter) | No WebKit on tvOS — there is no web view, in-app browser, or HTML rendering |

## Usage

The upstream plugins do **not** endorse a tvOS implementation, so add
the `*_tvos` package to your app **explicitly**, alongside the upstream
plugin:

```yaml
dependencies:
  shared_preferences: ^2.2.0
  shared_preferences_tvos:
    git:
      url: https://github.com/fluttertv/plugins.git
      path: packages/shared_preferences_tvos
```

Then use the upstream plugin's API exactly as on iOS — the tvOS
implementation registers automatically. Once published these become
plain `^version` dependencies.

A few packages need a writable directory and therefore also
`path_provider_tvos`: e.g. `video_player_tvos` (for
`VideoPlayerController.file`) and `sqflite_tvos` (for the database
path). Their READMEs note this.

---

# How this repository was created

These packages were not hand-written from scratch. They were produced
with the **`flutter-tvos plugin port`** tool (part of
[flutter-tvos](https://github.com/fluttertv/flutter-tvos)) and then
verified — and where needed finished — by hand. This is the exact,
reproducible workflow.

## 0. Prerequisites

```sh
# the flutter-tvos CLI (custom embedder + tooling)
git clone https://github.com/fluttertv/flutter-tvos.git
export TVOS=$PWD/flutter-tvos/bin/flutter-tvos
```

## 1. Port an upstream plugin

`flutter-tvos plugin port` takes an existing Apple plugin (the iOS or
macOS implementation package) and emits a federated `*_tvos` package.

```sh
# from a published pub.dev package (what we used):
$TVOS plugin port --from-pub video_player_avfoundation \
  --output plugins/packages/video_player_tvos --include-example

# or from git, or from a local path:
$TVOS plugin port --from-git https://github.com/foo/bar.git --ref main --output ...
$TVOS plugin port ../some_plugin_ios --output ...
```

The exact upstream source for each package is recorded at the top of
its `PORTING_REPORT.md` (e.g. `video_player_tvos` ←
`video_player_avfoundation`, `shared_preferences_tvos` ←
`shared_preferences_foundation`, `audioplayers_tvos` ←
`audioplayers_darwin`).

**What the porter does automatically:**

- Copies the upstream Dart `lib/` (rewriting `package:` self-imports)
  and federates through the upstream `*_platform_interface`.
- Copies the native Swift/Objective-C into `tvos/Classes/` and
  generates a tvOS `*.podspec` (no dependency on the Flutter
  CocoaPod — tvOS resolves `Flutter.framework` via search paths).
- Makes tvOS follow the iOS code paths: widens `#if os(iOS)` →
  `(os(iOS) || os(tvOS))`, ObjC `#if TARGET_OS_IOS` →
  `(TARGET_OS_IOS || TARGET_OS_TV)`, and `@available` / `#available`
  / `API_AVAILABLE` `iOS <v>` → also `tvOS <v>`.
- Collapses modern multi-target / `include/`-modular SwiftPM packages
  into one CocoaPods module (drops the macOS-only target).
- Sets `FLTAssetsPath` so plugin asset lookup resolves on a real
  Apple TV; sanitizes example pub-workspace / `dependency_overrides`
  wiring.
- **Graceful partial port:** an API that genuinely doesn't exist on
  tvOS, used at type/top-level scope, is wrapped in `#if !os(tvOS)` /
  `#if !TARGET_OS_TV` so the package still compiles with that feature
  disabled, and every such region is listed in `PORTING_REPORT.md`
  under "Disabled on tvOS". A compatibility database
  (WebKit, SafariServices, CoreLocation, CoreTelephony,
  `AVAudioSession` routing options, …) drives this.

## 2. Read the porting report

Every package gets a `PORTING_REPORT.md`: the source + version, the
tvOS build outlook, methods ported/stubbed, every disabled region with
the reason, and a checklist. Read it before trusting a port.

## 3. Verify

```sh
cd plugins/packages/<pkg>/example
flutter pub get
$TVOS build tvos --simulator --debug          # must be green
$TVOS test integration_test/<plugin>_test.dart -d <sim-udid>
# on a physical Apple TV (set your signing team):
DEVELOPMENT_TEAM=XXXXXXXXXX $TVOS run -d <device-udid>
```

Only a green simulator build (and, ideally, passing integration tests
on a real Apple TV) qualifies a package for this list.

## 4. Hand-finish where the porter can't

The porter is honest about its limits; some packages needed manual
work, all of it documented in their `PORTING_REPORT.md`:

- **`path_provider_tvos`** — `path_provider_foundation` is a
  dart:ffi/native-assets plugin the tvOS toolchain can't build, so the
  porter only emits a skeleton. A real native implementation
  (`NSSearchPathForDirectoriesInDomains` / `NSTemporaryDirectory`) was
  written by hand.
- **`flutter_secure_storage_tvos`** — Keychain works on tvOS; the
  optional `LAContext` / `.biometryAny` / Secure-Enclave biometric
  path (which tvOS lacks) was guarded out by hand.
- **`audioplayers_tvos`, `flutter_tts_tvos`** — `AVAudioSession`
  category options that don't exist on tvOS
  (`allowBluetooth`, `defaultToSpeaker`, …) were mapped to no-ops.
- **`sqflite_tvos`** — re-ported once the porter learned to collapse
  single-target `include/`-modular SwiftPM packages.

## 5. Curate

Packages whose **primary purpose** can't work on tvOS, or that don't
build after best-effort, are removed rather than published broken (see
[Evaluated but not provided](#evaluated-but-not-provided)).

See [`AUTHORING.md`](AUTHORING.md) for the deeper per-plugin recipe.

## Repository layout

```
plugins/
├── packages/<plugin>_tvos/    # one directory per plugin
│   ├── lib/                   # Dart (federated impl)
│   ├── tvos/Classes/          # native Swift/ObjC
│   ├── tvos/<plugin>.podspec  # CocoaPods spec, tvOS 13+
│   ├── example/               # runnable tvOS example
│   ├── PORTING_REPORT.md      # port detail + checklist
│   ├── README.md  CHANGELOG.md  LICENSE
└── AUTHORING.md               # how to add a new one
```

## Contributing

- Federate via the upstream `*_platform_interface`; suffix `_tvos`.
- Target tvOS 13.0+; guard shared iOS code with `#if os(tvOS)`.
- Document every API as ✅ supported / ⚠️ partial / ❌ unsupported in
  the package README (the most useful thing for users).
- A package only ships if it builds green on tvOS.

## License

BSD-3-Clause (see `LICENSE`). Ported packages retain their upstream
copyright; tvOS additions are © The FlutterTV Authors.
