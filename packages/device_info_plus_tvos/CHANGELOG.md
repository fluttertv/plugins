## 0.0.1

Initial release — tvOS implementation of `device_info_plus` for
[flutter-tvos](https://github.com/fluttertv/flutter-tvos). Generated
by `flutter-tvos plugin port`. Use `DeviceInfoPlugin().iosInfo` — the
tvOS device maps onto the iOS info shape (`UIDevice`, `utsname`).

* **Supported:** `name`, `systemName` (== `"tvOS"`), `systemVersion`,
  `model`, `localizedModel`, `identifierForVendor`,
  `isPhysicalDevice`, `utsname.*`, `systemFeatures`.
* **Differs from iOS:** `isiOSAppOnMac` / `isiOSAppOnVision` are
  always `false` — the underlying selectors do not exist on tvOS.
* **Not supported on tvOS:** iOS-app-on-Mac / iOS-app-on-Vision
  context flags (meaningless on tvOS).

See `README.md` and `PORTING_REPORT.md` for detail.
