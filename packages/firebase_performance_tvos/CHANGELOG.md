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

* Initial tvOS (Apple TV) implementation of `firebase_performance`, ported from
  `firebase_performance` 0.11.4+3 via `flutter-tvos plugin port` and finished by
  hand (podspec `Firebase/Performance` + `firebase_core_tvos` deps, tvOS 15.0
  floor, `firebase_core_tvos` import, generated `Package.swift` removed, Dart
  re-export).
* No tvOS feature disables — full Performance API (custom traces, HTTP metrics).
  Compiles + links + registers on the tvOS simulator and device (arm64).
