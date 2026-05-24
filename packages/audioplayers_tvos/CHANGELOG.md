## 0.0.1

Initial release — tvOS implementation of `audioplayers` for
[flutter-tvos](https://github.com/fluttertv/flutter-tvos). Ported from
`audioplayers_darwin` and hand-finished for tvOS.

* **Supported:** play / pause / stop / resume / seek / volume / playback
  rate / release; looping; asset, URL and byte sources
  (`AVPlayer` / `AVAudioPlayer`).
* **Differs from iOS:** `AVAudioSession` category options that don't
  exist on tvOS (`allowBluetooth`, `allowBluetoothA2DP`,
  `defaultToSpeaker`, `overrideMutedMicrophoneInterruption`) are
  accepted but have no effect — Apple TV routes audio over HDMI / eARC
  / AirPlay.
* **Not supported on tvOS:** Bluetooth / earpiece / speaker routing
  controls; microphone-related options.

On-device verification recommended for audio-routing edge cases. See
`README.md` and `PORTING_REPORT.md` for the full matrix.
