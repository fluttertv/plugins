# flutter_secure_storage_tvos

tvOS implementation of [`flutter_secure_storage`](https://pub.dev/packages/flutter_secure_storage)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos)
(port of `flutter_secure_storage_darwin`, hand-finished for tvOS).

> **Verified:** simulator build GREEN.

## Usage

```yaml
dependencies:
  flutter_secure_storage: ^10.x
  flutter_secure_storage_tvos:
    path: ../flutter_secure_storage_tvos   # or pub.dev once published
```

## tvOS support

### ✅ Supported
- `read` / `write` / `delete` / `readAll` / `deleteAll` /
  `containsKey` — full Keychain-backed secure storage (the Security
  framework is available on tvOS).
- Keychain accessibility options and access groups.

### ⚠️ Limitations / differs from iOS
- **Biometric / passcode-gated access control is a no-op on tvOS.**
  An Apple TV has no Face ID / Touch ID / device passcode, so
  `LAContext`, `.biometryAny`, `.biometryCurrentSet` and Secure-Enclave
  biometric reuse are compiled out. Items requesting those flags are
  still stored and readable — just without the (impossible) biometric
  gate. Do not rely on biometric protection on tvOS.

### ❌ Not supported on tvOS
- Local Authentication (biometrics) — does not exist on tvOS.

See `PORTING_REPORT.md` for the port detail and checklist.
