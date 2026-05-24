## 0.0.1

Initial release — tvOS implementation of `flutter_tts` for
[flutter-tvos](https://github.com/fluttertv/flutter-tvos). Ported
from `flutter_tts` and hand-finished for tvOS.

* **Supported:** `speak` / `stop` / `pause`, `setLanguage`,
  `setVoice`, `setSpeechRate`, `setVolume`, `setPitch`,
  `getLanguages`, `getVoices`, `awaitSpeakCompletion` —
  `AVSpeechSynthesizer` is available on tvOS.
* **Differs from iOS:** `AVAudioSession` category options that don't
  exist on tvOS (`allowBluetooth`, `allowBluetoothA2DP`,
  `defaultToSpeaker`) are accepted but have no effect — speech plays
  via the default HDMI / AirPlay route. No silent-switch / earpiece
  concept on tvOS.
* **Not supported on tvOS:** audio-routing category options (not
  applicable on an Apple TV).

See `README.md` and `PORTING_REPORT.md` for detail.
