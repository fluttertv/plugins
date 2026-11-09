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

- Initial tvOS (Apple TV) implementation of `firebase_analytics`, ported from
  `firebase_analytics` 12.4.3 via `flutter-tvos plugin port` and finished by
  hand (podspec `Firebase/Analytics` + `firebase_core_tvos` deps, tvOS 15.0
  floor, `firebase_core_tvos` import, Dart re-export).
- Verified on the tvOS simulator and a physical Apple TV 4K (tvOS 26.2):
  Firebase initializes and Analytics events reach the backend.
