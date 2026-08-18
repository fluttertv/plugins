## 0.0.1

* Initial tvOS (Apple TV) implementation of `firebase_remote_config`, ported from
  `firebase_remote_config` 6.5.3 with `flutter-tvos plugin port` and finished by
  hand. Full Remote Config API (defaults, fetch/activate/fetchAndActivate, typed
  getters, config settings, real-time updates); no tvOS feature disables.
* Native code aligned to the `firebase_core 4.11.x` /
  `firebase_core_platform_interface 7.1.0` FlutterFire train; depends on
  `firebase_core_tvos`.
