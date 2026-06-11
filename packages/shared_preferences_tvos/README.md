# shared_preferences_tvos

tvOS implementation of [`shared_preferences`](https://pub.dev/packages/shared_preferences)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos)
(port of `shared_preferences_foundation`).

> Hand-finished from `flutter-tvos plugin port`.
> **Verified:** 63/63 integration tests pass on a physical Apple TV.

## Usage

`shared_preferences` does not yet endorse a tvOS implementation, so add
this package directly alongside it:

```yaml
dependencies:
  shared_preferences: ^2.x
  shared_preferences_tvos: ^0.0.2
```

Use `shared_preferences` exactly as on iOS — the tvOS implementation
registers automatically (it is `NSUserDefaults`-backed).

## tvOS support

### ✅ Supported
- Full legacy API: `getString/Bool/Int/Double/StringList`, `set*`,
  `remove`, `clear`, `getKeys`, `reload`.
- Full `SharedPreferencesAsync` / `withCache` API.
- Persistence across launches (backed by `NSUserDefaults`, which exists
  on tvOS).

### ❌ Not supported on tvOS
- None. This plugin is fully functional on tvOS.

See `PORTING_REPORT.md` for the port detail and checklist.

## Dependency management

Supports both **Swift Package Manager** and **CocoaPods** from a single
source tree. `flutter-tvos` wires the right one automatically: apps on
Flutter 3.44+ link it via SwiftPM (this package ships a `tvos/Package.swift`),
while CocoaPods-based projects keep using the podspec. No manual setup needed.
