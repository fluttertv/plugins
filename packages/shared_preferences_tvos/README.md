# shared_preferences_tvos

tvOS implementation of [`shared_preferences`](https://pub.dev/packages/shared_preferences)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos)
(port of `shared_preferences_foundation`).

> Hand-finished from `flutter-tvos plugin port`.
> **Verified:** simulator build GREEN **and** 63/63 integration tests
> pass on a physical Apple TV.

## Usage

`shared_preferences` does not yet endorse a tvOS implementation, so add
this package directly alongside it:

```yaml
dependencies:
  shared_preferences: ^2.x
  shared_preferences_tvos:
    path: ../shared_preferences_tvos   # or pub.dev once published
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
