## 0.0.2

* Add Swift Package Manager support: ships a `tvos/Package.swift` so the
  package can be consumed via SwiftPM (the Flutter 3.44 default) alongside the
  existing CocoaPods podspec. No API or behaviour change.

## 0.0.1

Initial release — tvOS implementation of `package_info_plus` for
[flutter-tvos](https://github.com/fluttertv/flutter-tvos). Generated
by `flutter-tvos plugin port`.

* **Supported:** `appName`, `packageName`, `version`, `buildNumber`,
  `buildSignature` — read from the app bundle `Info.plist`
  (available on tvOS).
* **Differs from iOS:** `installerStore` is `null` on tvOS (no App
  Store installer-source attribution exposed).
* **Not supported on tvOS:** none for core fields.

See `README.md` and `PORTING_REPORT.md` for detail.
