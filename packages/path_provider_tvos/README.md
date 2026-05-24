# path_provider_tvos

tvOS implementation of [`path_provider`](https://pub.dev/packages/path_provider)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos).

> **Hand-written, maintained** tvOS implementation. The upstream
> `path_provider_foundation` is a dart:ffi/native-assets plugin that the
> tvOS toolchain cannot build, so this is not generated output.
> **Verified:** simulator build GREEN **and** exercised on a physical
> Apple TV via `video_player_tvos` (14/14).

## Usage

```yaml
dependencies:
  path_provider: ^2.x
  path_provider_tvos: ^0.0.1
```

## tvOS support

### ✅ Supported
- `getTemporaryDirectory()` — `NSTemporaryDirectory()`
- `getApplicationDocumentsDirectory()` — app `Documents/`
- `getApplicationSupportDirectory()` — `Library/Application Support/`
  (auto-created)
- `getApplicationCacheDirectory()` — `Library/Caches/` (auto-created)
- `getLibraryDirectory()` — app `Library/`

### ❌ Not supported on tvOS
- `getDownloadsDirectory()` → returns `null` (no user Downloads dir).
- `getExternalStorage*` → `UnsupportedError` (Android-only, same as iOS).

See `PORTING_REPORT.md` for detail.
