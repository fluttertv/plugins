# video_player_tvos

tvOS implementation of [`video_player`](https://pub.dev/packages/video_player)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos)
(port of `video_player_avfoundation`).

> Hand-finished from `flutter-tvos plugin port`.
> **Verified:** 14/14 integration tests pass on a physical Apple TV;
> video frames render via the external-texture path on real hardware.

## Usage

```yaml
dependencies:
  video_player: ^2.x
  video_player_tvos: ^0.0.1
  # Required only if you use VideoPlayerController.file with a temp path:
  path_provider_tvos: ^0.0.1
```

## tvOS support

### ✅ Supported
- Asset, network (`networkUrl`), and file (`file`) sources.
- Play / pause / seek / volume / playback speed / looping.
- Texture-backed rendering (`AVPlayer` + `FlutterTexture`) — verified
  on a real Apple TV.

### ⚠️ Limitations / differs from iOS
- `VideoPlayerController.file` with a temporary path needs a working
  `path_provider` on tvOS — use the bundled `path_provider_tvos`.
- The tvOS Simulator has no network; test remote URLs on a device.

### ❌ Not supported on tvOS
- None for core playback. Caption/track UI differences follow tvOS
  AVKit behaviour.

See `PORTING_REPORT.md` for the port detail and checklist.
