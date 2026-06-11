## 0.0.2

* Add Swift Package Manager support: ships a `tvos/Package.swift` so the
  package can be consumed via SwiftPM (the Flutter 3.44 default) alongside the
  existing CocoaPods podspec. No API or behaviour change.

## 0.0.1

Initial release — tvOS implementation of `shared_preferences` for
[flutter-tvos](https://github.com/fluttertv/flutter-tvos). Ported
from `shared_preferences_foundation` and hand-finished for tvOS.

* **Supported:** full legacy API (`getString/Bool/Int/Double/StringList`,
  `set*`, `remove`, `clear`, `getKeys`, `reload`) **and** the full
  `SharedPreferencesAsync` / `withCache` API. Persistence across
  launches via `NSUserDefaults` (available on tvOS).
* **Not supported on tvOS:** none. This plugin is fully functional.

Verified end-to-end on a physical Apple TV — **63/63 integration
tests pass**. See `README.md` and `PORTING_REPORT.md` for detail.

`shared_preferences` does not yet endorse a tvOS implementation, so
consumers must add `shared_preferences_tvos` to their app's `pubspec`
alongside `shared_preferences` (the federated registrar will pick it
up automatically).
