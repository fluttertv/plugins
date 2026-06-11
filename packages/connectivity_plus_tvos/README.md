# connectivity_plus_tvos

tvOS implementation of [`connectivity_plus`](https://pub.dev/packages/connectivity_plus)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos).

> Hand-finished from `flutter-tvos plugin port`.
> **Verified:** integration tests pass on a physical Apple TV.

## Usage

```yaml
dependencies:
  connectivity_plus: ^7.x
  connectivity_plus_tvos: ^0.0.2
```

## tvOS support

### ✅ Supported
- `checkConnectivity()` and `onConnectivityChanged` — backed by
  `NWPathMonitor`, which works on tvOS.
- Results: `wifi`, `ethernet`, `vpn`, `none`.

### ⚠️ Limitations / differs from iOS
- **No `mobile` / cellular result** — an Apple TV has no cellular
  radio. Wired Apple TVs report `ethernet`.

### ❌ Not supported on tvOS
- Cellular detection (not applicable).

See `PORTING_REPORT.md` for the port detail and checklist.

## Dependency management

Supports both **Swift Package Manager** and **CocoaPods** from a single
source tree. `flutter-tvos` wires the right one automatically: apps on
Flutter 3.44+ link it via SwiftPM (this package ships a `tvos/Package.swift`),
while CocoaPods-based projects keep using the podspec. No manual setup needed.
