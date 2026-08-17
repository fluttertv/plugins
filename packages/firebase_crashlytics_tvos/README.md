# firebase_crashlytics_tvos

The tvOS implementation of [`firebase_crashlytics`](https://pub.dev/packages/firebase_crashlytics).

> Ported with [`flutter-tvos plugin port`](https://github.com/fluttertv/flutter-tvos)
> from `firebase_crashlytics` 5.2.4, then finished + verified by hand. See
> `PORTING_REPORT.md`.

## Usage

Federated plugin implementation — no imports needed from app code; it registers
automatically. Apps that already use `firebase_crashlytics` and target tvOS add:

```yaml
dependencies:
    firebase_crashlytics: ^5.2.4
    firebase_crashlytics_tvos: ^0.0.1
    firebase_core: ^4.11.0
    firebase_core_tvos: ^0.0.1 # tvOS core (this package depends on it)
```

> **Version alignment matters.** This package's native code matches the
> `firebase_core_platform_interface` **7.1.0** train (`firebase_core 4.11.x`).
> Keep your whole Firebase stack on one consistent FlutterFire release, or Dart
> `initializeApp(options:)` can crash in `CoreFirebaseOptions.fromList` at launch
> (a `FirebaseOptions` field-count mismatch).

## Status

| Platform                                | Implemented | Verified                                                    |
| --------------------------------------- | ----------- | ----------------------------------------------------------- |
| Apple TV (`appletvos`)                  | yes         | ✅ **runtime-verified on a physical Apple TV 4K (release/AOT)** — a forced `crash()` was captured and reported to the Crashlytics console |
| Apple TV simulator (`appletvsimulator`) | yes         | ✅ runtime-verified — crash reported to the console |

All `firebase_crashlytics` Dart APIs work on tvOS. Ordinary crashes are captured
(signal + `NSException` handlers), but tvOS has no alternate signal stack, so
stack-overflow crashes may be missed, and the Mach exception server is off.
Crashes upload on the **next app launch** — force a crash, relaunch, then check
the console.

## Symbolication (dSYM)

Native crash frames need dSYM upload on every Apple platform. iOS wires this
automatically; this tvOS port doesn't (the auto step needs a `.symlinks` path the
flutter-tvos layout lacks). dSYMs are still produced (the podspec sets
`dwarf-with-dsym`) — just add a Run Script phase to your app's Runner target that
runs `"${PODS_ROOT}/FirebaseCrashlytics/run"`. Dart `recordError` reports are
already symbolicated.

## License

fluttertv under a BSD-3-Clause license. See `LICENSE` for the full text.
