# device_info_plus_tvos

tvOS implementation of [`device_info_plus`](https://pub.dev/packages/device_info_plus)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos).

> Hand-finished from `flutter-tvos plugin port`.
> **Verified:** simulator build GREEN.

## Usage

```yaml
dependencies:
  device_info_plus: ^13.x
  device_info_plus_tvos: ^0.0.1
```

Use `DeviceInfoPlugin().iosInfo` — the tvOS device maps onto the iOS
info shape (`utsname`, `UIDevice`).

## tvOS support

### ✅ Supported
- `name`, `systemName`, `systemVersion`, `model`, `localizedModel`,
  `identifierForVendor`, `isPhysicalDevice`, `utsname.*`,
  `systemFeatures`.

### ⚠️ Limitations / differs from iOS
- `isiOSAppOnMac` / `isiOSAppOnVision` are always `false` (not
  applicable to tvOS; the underlying selectors do not exist there).

### ❌ Not supported on tvOS
- iOS-app-on-Mac/Vision context flags (meaningless on tvOS).

See `PORTING_REPORT.md` for the port detail and checklist.
