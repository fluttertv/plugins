# firebase_analytics_tvos

The tvOS implementation of [`firebase_analytics`](https://pub.dev/packages/firebase_analytics).

> Ported with [`flutter-tvos plugin port`](https://github.com/fluttertv/flutter-tvos)
> from `firebase_analytics` 12.4.3, then finished + verified by hand. See
> `PORTING_REPORT.md`.

## Usage

Federated plugin implementation — no imports needed from app code; it registers
automatically. Apps that already use `firebase_analytics` and target tvOS add:

```yaml
dependencies:
    firebase_analytics: ^12.4.3
    firebase_analytics_tvos: ^0.0.1
    firebase_core: ^4.11.0
    firebase_core_tvos: ^0.0.1 # tvOS core (this package depends on it)
```

> **Version alignment matters.** This package's native code matches the
> `firebase_core_platform_interface` **7.1.0** train (`firebase_core 4.11.x`).
> Keep your whole Firebase stack on one consistent FlutterFire release, or Dart
> `initializeApp(options:)` can crash in `CoreFirebaseOptions.fromList` at launch
> (a `FirebaseOptions` field-count mismatch). See `PORTING_REPORT.md`.

## Status

| Platform                                | Implemented | Verified                                                                      |
| --------------------------------------- | ----------- | ----------------------------------------------------------------------------- |
| Apple TV (`appletvos`)                  | yes         | ✅ physical Apple TV 4K, tvOS 26.2 — Firebase inits, events reach the backend |
| Apple TV simulator (`appletvsimulator`) | yes         | ✅ builds + runs                                                              |

All `firebase_analytics` APIs are available (no tvOS feature disables). Events
appear in Firebase **DebugView** when the app is launched with `-FIRDebugEnabled`.

## License

fluttertv under a BSD-3-Clause license. See `LICENSE` for the full text.
