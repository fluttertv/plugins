# package_info_plus_tvos

tvOS implementation of [`package_info_plus`](https://pub.dev/packages/package_info_plus)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos).

> Hand-finished from `flutter-tvos plugin port`.

## Usage

```yaml
dependencies:
  package_info_plus: ^10.x
  package_info_plus_tvos: ^0.0.2
```

## tvOS support

### ✅ Supported
- `appName`, `packageName`, `version`, `buildNumber`,
  `buildSignature` — read from the app bundle `Info.plist`
  (available on tvOS).

### ⚠️ Limitations / differs from iOS
- `installerStore` is `null` on tvOS (no App Store installer source
  attribution exposed).

### ❌ Not supported on tvOS
- None for core fields.

See `PORTING_REPORT.md` for the port detail and checklist.

## Dependency management

This package ships a `tvos/Package.swift`. `flutter-tvos` links any plugin
that has one through **Swift Package Manager** and leaves it out of the
Podfile, so the podspec is only read by tools that do not know about SwiftPM.
No manual setup needed.
