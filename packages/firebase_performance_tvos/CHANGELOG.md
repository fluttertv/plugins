## 0.0.1

* Initial tvOS (Apple TV) implementation of `firebase_performance`, ported from
  `firebase_performance` 0.11.4+3 via `flutter-tvos plugin port` and finished by
  hand (podspec `Firebase/Performance` + `firebase_core_tvos` deps, tvOS 15.0
  floor, `firebase_core_tvos` import, generated `Package.swift` removed, Dart
  re-export).
* No tvOS feature disables — full Performance API (custom traces, HTTP metrics).
  Compiles + links + registers on the tvOS simulator and device (arm64).
