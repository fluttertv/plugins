# firebase_remote_config_tvos

The tvOS implementation of [`firebase_remote_config`](https://pub.dev/packages/firebase_remote_config).

> Ported with [`flutter-tvos plugin port`](https://github.com/fluttertv/flutter-tvos)
> from `firebase_remote_config` 6.5.3, then finished + verified by hand. See
> `PORTING_REPORT.md`.

## Usage

Federated plugin implementation — no imports needed from app code; it registers
automatically. Apps that already use `firebase_remote_config` and target tvOS add:

```yaml
dependencies:
    firebase_remote_config: ^6.5.3
    firebase_remote_config_tvos: ^0.0.1
    firebase_core: ^4.11.0
    firebase_core_tvos: ^0.0.1 # tvOS core (this package depends on it)
```

> **Version alignment matters.** This package's native code matches the
> `firebase_core_platform_interface` **7.1.0** train (`firebase_core 4.11.x`).
> Keep your whole Firebase stack on one consistent FlutterFire release, or Dart
> `initializeApp(options:)` can crash in `CoreFirebaseOptions.fromList` at launch
> (a `FirebaseOptions` field-count mismatch).

## Status

| Platform                                | Implemented | Verified                                                                                                                                                                                                                                                                                         |
| --------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Apple TV (`appletvos`)                  | yes         | ✅ verified on a **physical Apple TV 4K** (tvOS 26.2, release/AOT) — a parameter published in the **Firebase console** was fetched and activated on the device; the on-device `RemoteConfig.sqlite3` shows the console value in both the fetched and active tables, overriding the local default |
| Apple TV simulator (`appletvsimulator`) | yes         | ✅ verified end-to-end — a parameter published in the **Firebase console** was fetched by the Apple TV app (`fetchAndActivate` → `RemoteConfigFetchStatus.success`) and the server value overrode the local default via `getString`                                                              |

All `firebase_remote_config` APIs are available (no tvOS feature disables) —
defaults, `fetch`/`activate`/`fetchAndActivate`, typed getters, config settings,
and real-time config updates.

## License

fluttertv under a BSD-3-Clause license. See `LICENSE` for the full text.
