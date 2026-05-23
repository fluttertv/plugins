## 0.0.1

Initial release — tvOS implementation of `video_player` for
[flutter-tvos](https://github.com/fluttertv/flutter-tvos). Ported
from `video_player_avfoundation` and hand-finished for tvOS.

* **Supported:** asset, network (`networkUrl`) and file (`file`)
  sources; play / pause / seek / volume / playback speed / looping;
  texture-backed rendering (`AVPlayer` + `FlutterTexture`).
* **Differs from iOS:** `VideoPlayerController.file` with a temporary
  path needs a working `path_provider` on tvOS — use the bundled
  `path_provider_tvos`. The tvOS Simulator has no network — test
  remote URLs on a device. Caption / track UI differences follow
  tvOS AVKit behaviour.
* **Not supported on tvOS:** none for core playback.

Verified end-to-end on a physical Apple TV — **14/14 integration
tests pass**; video frames render via the external-texture path on
real hardware. See `README.md` and `PORTING_REPORT.md` for detail.
