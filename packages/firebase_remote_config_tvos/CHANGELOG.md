## 0.0.2

* Add Swift Package Manager support: ships `tvos/Package.swift` (one Swift
  target, with `firebase_core_tvos` as the sibling package
  `../firebase_core_tvos`). flutter-tvos links a plugin that ships
  `tvos/Package.swift` through Swift Package Manager and leaves it out of the
  Podfile.
* Requires `firebase_core_tvos: ^0.0.4`, the first version with a
  `tvos/Package.swift`. firebase_core_tvos 0.0.4 is no longer in the Podfile, so
  this package's podspec could not resolve its `firebase_core_tvos` dependency.

## 0.0.1

* Initial tvOS (Apple TV) implementation of `firebase_remote_config`, ported from
  `firebase_remote_config` 6.5.3 with `flutter-tvos plugin port` and finished by
  hand. Full Remote Config API (defaults, fetch/activate/fetchAndActivate, typed
  getters, config settings, real-time updates); no tvOS feature disables.
* Native code aligned to the `firebase_core 4.11.x` /
  `firebase_core_platform_interface 7.1.0` FlutterFire train; depends on
  `firebase_core_tvos`.
