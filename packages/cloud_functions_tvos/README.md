# cloud_functions_tvos

The tvOS implementation of [`cloud_functions`](https://pub.dev/packages/cloud_functions).

> Ported with [`flutter-tvos plugin port`](https://github.com/fluttertv/flutter-tvos)
> from `cloud_functions` 6.3.3, then finished + verified by hand. See
> `PORTING_REPORT.md`.

## Usage

Federated plugin implementation — no imports needed from app code; it registers
automatically. Apps that already use `cloud_functions` and target tvOS add:

```yaml
dependencies:
  cloud_functions: ^6.3.3
  cloud_functions_tvos: ^0.0.1
  firebase_core: ^4.11.0
  firebase_core_tvos: ^0.0.1 # tvOS core (this package depends on it)
```

> **Version alignment matters.** This package's native code matches the
> `firebase_core_platform_interface` **7.1.0** train (`firebase_core 4.11.x`).
> Keep your whole Firebase stack on one consistent FlutterFire release, or Dart
> `initializeApp(options:)` can crash in `CoreFirebaseOptions.fromList` at launch
> (a `FirebaseOptions` field-count mismatch).

## Status

| Platform | Implemented | Verified |
| --- | --- | --- |
| Apple TV (`appletvos`) | yes | ✅ verified on a **physical Apple TV 4K** (tvOS 26.6, release/AOT) — a callable function round-tripped against a live Firebase project |
| Apple TV simulator (`appletvsimulator`) | yes | ✅ verified — same callable round-trip |

Full `cloud_functions` API is available on tvOS (callable functions +
streaming callables, `httpsCallable`, region/emulator selection), no feature
disables. Streaming requires tvOS 15+ (the pod floor).

## License

fluttertv under a BSD-3-Clause license. See `LICENSE` for the full text.
