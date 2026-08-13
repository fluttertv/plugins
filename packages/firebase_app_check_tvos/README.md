# firebase_app_check_tvos

The tvOS implementation of [`firebase_app_check`](https://pub.dev/packages/firebase_app_check).

> Ported with [`flutter-tvos plugin port`](https://github.com/fluttertv/flutter-tvos)
> from `firebase_app_check` 0.4.5, then finished + verified by hand. See
> `PORTING_REPORT.md`.

## Usage

Federated plugin implementation — no imports needed from app code; it registers
automatically. Apps that already use `firebase_app_check` and target tvOS add:

```yaml
dependencies:
  firebase_app_check: ^0.4.5
  firebase_app_check_tvos: ^0.0.1
  firebase_core: ^4.11.0
  firebase_core_tvos: ^0.0.1 # tvOS core (this package depends on it)
```

Use the Apple providers that exist on tvOS 15+ — **DeviceCheck** or **App Attest**:

```dart
await FirebaseAppCheck.instance.activate(
  providerApple: const AppleDeviceCheckProvider(),
  // or: const AppleAppAttestProvider(), AppleAppAttestWithDeviceCheckFallbackProvider()
);
```

> **Version alignment matters.** This package's native code matches the
> `firebase_core_platform_interface` **7.1.0** train (`firebase_core 4.11.x`).
> Keep your whole Firebase stack on one consistent FlutterFire release, or Dart
> `initializeApp(options:)` can crash in `CoreFirebaseOptions.fromList` at launch
> (a `FirebaseOptions` field-count mismatch).

## tvOS provider support

| Provider | tvOS |
| --- | --- |
| **DeviceCheck** (`AppleDeviceCheckProvider`) | ✅ (tvOS 15+) |
| **App Attest** (`AppleAppAttestProvider`, …WithDeviceCheckFallback) | ✅ (tvOS 15+) |
| **Debug** (`AppleDebugProvider`) | ✅ (use on the simulator) |
| **reCAPTCHA** (`AppleReCaptchaProvider`) | ❌ **not available** — `RecaptchaProvider` is iOS-only in the Firebase Apple SDK; not an Apple-TV provider. Requesting it on tvOS leaves the provider unconfigured and `getToken` surfaces an explicit error. |

DeviceCheck / App Attest attestation runs on **real Apple TV hardware** (not the
simulator — use the Debug provider there).

## Status

| Platform | Implemented | Verified |
| --- | --- | --- |
| Apple TV (`appletvos`) | yes | ⏳ pending physical Apple TV pass (DeviceCheck runs only on real hardware) |
| Apple TV simulator (`appletvsimulator`) | yes | ✅ verified — native `FirebaseAppCheck 12.15.0` initializes on tvOS, the Debug provider issues a token, and `getToken` round-trips to the App Check backend (`exchangeDebugToken`) via the Pigeon channel |

## License

fluttertv under a BSD-3-Clause license. See `LICENSE` for the full text.
