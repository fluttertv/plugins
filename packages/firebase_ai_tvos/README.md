# firebase_ai_tvos

The tvOS implementation of [`firebase_ai`](https://pub.dev/packages/firebase_ai).

> Ported with [`flutter-tvos plugin port`](https://github.com/fluttertv/flutter-tvos)
> from `firebase_ai` 3.13.1, then finished + verified by hand. See
> `PORTING_REPORT.md`.

## Usage

Federated plugin implementation — no imports needed from app code; it registers
automatically. Apps that already use `firebase_ai` and target tvOS add:

```yaml
dependencies:
  firebase_ai: ^3.13.1
  firebase_ai_tvos: ^0.0.1
  firebase_core: ^4.11.0
  firebase_core_tvos: ^0.0.1 # for Firebase.initializeApp on tvOS
```

> **Version alignment.** This package tracks `firebase_ai 3.13.1`, which is on the
> `firebase_core 4.11.x` train. Keep your whole Firebase stack on one consistent
> FlutterFire release (the same train as `firebase_core_tvos`).

`firebase_ai`'s heavy lifting (Gemini / Imagen requests) happens in **Dart over
HTTPS**, so it works on tvOS unchanged. Its native layer is tiny — a single
method channel that returns the app's bundle identifier — so this package has
**no Firebase native SDK dependency** and does not depend on `firebase_core_tvos`
itself (your app still needs `firebase_core_tvos` for `Firebase.initializeApp`).

## Status

| Platform | Implemented | Verified |
| --- | --- | --- |
| Apple TV (`appletvos`) | yes | ✅ verified on a **physical Apple TV 4K** (tvOS 26.x, release/AOT) — `generateContent` reached the Gemini backend and was authenticated + model-resolved on-device |
| Apple TV simulator (`appletvsimulator`) | yes | ✅ verified — same authenticated `generateContent` round-trip against a live project |

Full `firebase_ai` API is available on tvOS (Gemini Developer API via
`FirebaseAI.googleAI()` and Vertex AI via `FirebaseAI.vertexAI()`), no feature
disables. The request round-trip (native registration → Dart → Gemini backend →
authenticated response) is verified on device and simulator; returning generated
content additionally requires the Firebase project to have Gemini API
billing/credits available.

## License

fluttertv under a BSD-3-Clause license. See `LICENSE` for the full text.
