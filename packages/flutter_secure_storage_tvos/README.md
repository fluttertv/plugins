# flutter_secure_storage_tvos

tvOS implementation of [`flutter_secure_storage`](https://pub.dev/packages/flutter_secure_storage)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos)
(port of `flutter_secure_storage_darwin`, hand-finished for tvOS).

## Usage

```yaml
dependencies:
  flutter_secure_storage: ^10.x
  flutter_secure_storage_tvos: ^0.0.2
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

## Dependency management

Supports both **Swift Package Manager** and **CocoaPods** from a single
source tree. `flutter-tvos` wires the right one automatically: apps on
Flutter 3.44+ link it via SwiftPM (this package ships a `tvos/Package.swift`),
while CocoaPods-based projects keep using the podspec. No manual setup needed.
