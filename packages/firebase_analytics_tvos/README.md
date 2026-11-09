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
    firebase_analytics_tvos: ^0.0.2
    firebase_core: ^4.11.0
    firebase_core_tvos: ^0.0.4 # tvOS core (this package depends on it)
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

All `firebase_analytics` APIs work on tvOS **except**
`initiateOnDeviceConversionMeasurement`, which is iOS-only
(`API_UNAVAILABLE(tvos)`; its backing `GoogleAdsOnDeviceConversion` SDK is
iOS-only). The handler is kept verbatim from upstream, so on tvOS that call is a
**no-op** — it returns without error but sends no conversion data; don't build an
on-device-conversion flow against it on tvOS. Events appear in Firebase
**DebugView** when the app is launched with `-FIRDebugEnabled`.

## Swift Package Manager

This package ships a `tvos/Package.swift`. flutter-tvos links a plugin that
ships `tvos/Package.swift` through Swift Package Manager and leaves it out of
the Podfile. No manual setup is needed. It depends on `firebase_core_tvos`
0.0.4, which ships one too, and takes firebase-ios-sdk `~> 12.15.0`, as in the
podspec.

Needs flutter-tvos 1.3.0 or later, the first release that links plugins through
SwiftPM, places them side by side (so `../firebase_core_tvos` and
`../FlutterFramework` resolve) and leaves them out of the Podfile.

## License

fluttertv under a BSD-3-Clause license. See `LICENSE` for the full text.
