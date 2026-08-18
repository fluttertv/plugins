## 0.0.1

* Initial tvOS (Apple TV) implementation of `firebase_crashlytics`, ported from
  `firebase_crashlytics` 5.2.4 via `flutter-tvos plugin port` and finished by
  hand (podspec `Firebase/Crashlytics` + `firebase_core_tvos` deps, tvOS 15.0
  floor, `LIBRARY_NAME`/`LIBRARY_VERSION` defines, `firebase_core_tvos` imports,
  Dart re-export).
* No tvOS feature disables — full Crashlytics API. Compiles + links + registers
  on the tvOS simulator and device (arm64).
