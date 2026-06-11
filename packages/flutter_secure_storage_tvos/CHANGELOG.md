## 0.0.2

* Add Swift Package Manager support: ships a `tvos/Package.swift` so the
  package can be consumed via SwiftPM (the Flutter 3.44 default) alongside the
  existing CocoaPods podspec. No API or behaviour change.

## 0.0.1

Initial release — tvOS implementation of `flutter_secure_storage`
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos). Ported
from `flutter_secure_storage_darwin` and hand-finished for tvOS.

* **Supported:** `read` / `write` / `delete` / `readAll` /
  `deleteAll` / `containsKey` — full Keychain-backed secure storage
  (Security framework is available on tvOS). Keychain accessibility
  options and access groups.
* **Differs from iOS:** **biometric / passcode-gated access control
  is a no-op on tvOS.** Apple TV has no Face ID / Touch ID / device
  passcode, so `LAContext`, `.biometryAny`, `.biometryCurrentSet` and
  Secure-Enclave biometric reuse are compiled out. Items requesting
  those flags are still stored and readable — just without the
  (impossible) biometric gate. Do not rely on biometric protection on
  tvOS.
* **Not supported on tvOS:** LocalAuthentication framework
  (biometrics) — does not exist on tvOS.

See `README.md` and `PORTING_REPORT.md` for detail.
