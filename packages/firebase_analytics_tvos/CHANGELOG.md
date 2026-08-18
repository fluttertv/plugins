## 0.0.1

- Initial tvOS (Apple TV) implementation of `firebase_analytics`, ported from
  `firebase_analytics` 12.4.3 via `flutter-tvos plugin port` and finished by
  hand (podspec `Firebase/Analytics` + `firebase_core_tvos` deps, tvOS 15.0
  floor, `firebase_core_tvos` import, Dart re-export).
- Verified on the tvOS simulator and a physical Apple TV 4K (tvOS 26.2):
  Firebase initializes and Analytics events reach the backend.
