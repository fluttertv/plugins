# wakelock_plus_tvos

tvOS implementation of [`wakelock_plus`](https://pub.dev/packages/wakelock_plus)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos).

> Hand-finished from `flutter-tvos plugin port`.
> **Verified:** 2/2 integration tests pass on a physical Apple TV.

## Usage

```yaml
dependencies:
  wakelock_plus: ^1.x
  wakelock_plus_tvos: ^0.0.1
```

## tvOS support

### ✅ Supported
- `WakelockPlus.enable()` / `disable()` / `toggle()` / `enabled` —
  backed by `UIApplication.isIdleTimerDisabled`, which exists on tvOS
  (keeps the Apple TV screensaver from kicking in).

### ❌ Not supported on tvOS
- None. Fully functional.

See `PORTING_REPORT.md` for the port detail and checklist.
