## 0.0.1

* Initial tvOS (Apple TV) implementation of `firebase_ai`, ported from
  `firebase_ai` 3.13.1 with `flutter-tvos plugin port` and finished by hand.
  Full API (Gemini Developer API via `FirebaseAI.googleAI()` and Vertex AI via
  `FirebaseAI.vertexAI()`); no tvOS feature disables.
* Native layer is a single method channel (`getPlatformHeaders`) — no Firebase
  native SDK dependency. Tracks the `firebase_core 4.11.x` FlutterFire train.
