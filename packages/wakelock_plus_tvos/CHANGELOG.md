## 0.0.1

Initial release — tvOS implementation of `wakelock_plus` for
[flutter-tvos](https://github.com/fluttertv/flutter-tvos). Generated
by `flutter-tvos plugin port`.

* **Supported:** `WakelockPlus.enable()` / `disable()` / `toggle()` /
  `enabled` — backed by `UIApplication.isIdleTimerDisabled`, which
  exists on tvOS (keeps the Apple TV screensaver from kicking in).
* **Not supported on tvOS:** none. This plugin is fully functional.

Verified end-to-end on a physical Apple TV — **2/2 integration tests
pass**. See `README.md` and `PORTING_REPORT.md` for detail.
