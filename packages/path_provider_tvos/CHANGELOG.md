## 0.0.2

* Add Swift Package Manager support: ships a `tvos/Package.swift` so the
  package can be consumed via SwiftPM (the Flutter 3.44 default) alongside the
  existing CocoaPods podspec. No API or behaviour change.

## 0.0.1

Initial release — **hand-written, maintained** tvOS implementation of
`path_provider` for
[flutter-tvos](https://github.com/fluttertv/flutter-tvos). Upstream
`path_provider_foundation` is a `dart:ffi` / native-assets plugin that
the tvOS toolchain cannot build, so this package is not generated
output — it is a thin native (`NSSearchPath…` / `NSTemporaryDirectory`)
implementation answering the same method-channel contract.

* **Supported:** `getTemporaryDirectory()`,
  `getApplicationDocumentsDirectory()`,
  `getApplicationSupportDirectory()` (auto-created),
  `getApplicationCacheDirectory()` (auto-created),
  `getLibraryDirectory()`.
* **Not supported on tvOS:** `getDownloadsDirectory()` returns `null`
  (no user Downloads dir in the tvOS sandbox);
  `getExternalStoragePath*` / `getExternalCachePaths` throw
  `UnsupportedError` (Android-only, same as iOS).

Verified end-to-end on a physical Apple TV via `video_player_tvos`
(14/14 integration tests). See `README.md` and `PORTING_REPORT.md`
for detail.
