# firebase_performance_tvos

The tvOS implementation of [`firebase_performance`](https://pub.dev/packages/firebase_performance).

> Ported with [`flutter-tvos plugin port`](https://github.com/fluttertv/flutter-tvos)
> from `firebase_performance` 0.11.4+3, then finished + verified by hand. See
> `PORTING_REPORT.md`.

## Usage

Federated plugin implementation — no imports needed from app code; it registers
automatically. Apps that already use `firebase_performance` and target tvOS add:

```yaml
dependencies:
    firebase_performance: ^0.11.4+3
    firebase_performance_tvos: ^0.0.2
    firebase_core: ^4.11.0
    firebase_core_tvos: ^0.0.4 # tvOS core (this package depends on it)
```

> **Version alignment matters.** This package's native code matches the
> `firebase_core_platform_interface` **7.1.0** train (`firebase_core 4.11.x`).
> Keep your whole Firebase stack on one consistent FlutterFire release, or Dart
> `initializeApp(options:)` can crash in `CoreFirebaseOptions.fromList` at launch
> (a `FirebaseOptions` field-count mismatch).

## Status

| Platform                                | Implemented | Verified                                                                                                                                          |
| --------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Apple TV (`appletvos`)                  | yes         | ✅ **verified on a physical Apple TV 4K (release/AOT)** — a custom trace was confirmed in the Performance dashboard (`tvos_device_trace`, 207 ms) |
| Apple TV simulator (`appletvsimulator`) | yes         | ✅ verified — trace + HTTP metric confirmed in the Performance dashboard (`tvos_smoke_trace`, 206 ms)                                             |

All `firebase_performance` APIs are available (no tvOS feature disables) —
custom traces + HTTP metrics. (Performance dashboard data is batched and can take
up to ~12h to appear; the console log confirms capture immediately.)

## Swift Package Manager

This package ships a `tvos/Package.swift`. flutter-tvos links a plugin that
ships `tvos/Package.swift` through Swift Package Manager and leaves it out of
the Podfile. No manual setup is needed. It depends on `firebase_core_tvos`
0.0.4, which ships one too, and takes firebase-ios-sdk `~> 12.15.0`, as in the
podspec.

## License

fluttertv under a BSD-3-Clause license. See `LICENSE` for the full text.
