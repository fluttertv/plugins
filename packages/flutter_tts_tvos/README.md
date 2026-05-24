# flutter_tts_tvos

tvOS implementation of [`flutter_tts`](https://pub.dev/packages/flutter_tts)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos)
(hand-finished for tvOS).

> On-device verification recommended for audio-routing edge cases.

## Usage

```yaml
dependencies:
  flutter_tts: ^4.x
  flutter_tts_tvos: ^0.0.1
```

## tvOS support

### ✅ Supported
- `speak` / `stop` / `pause`, `setLanguage`, `setVoice`,
  `setSpeechRate`, `setVolume`, `setPitch`, `getLanguages`,
  `getVoices`, `awaitSpeakCompletion` — `AVSpeechSynthesizer` is
  available on tvOS.

### ⚠️ Limitations / differs from iOS
- `AVAudioSession` category options that don't exist on tvOS
  (`allowBluetooth`, `allowBluetoothA2DP`, `defaultToSpeaker`) are
  accepted but have **no effect** — speech plays via the default
  HDMI/AirPlay route.
- No silent-switch / earpiece concept on tvOS.

### ❌ Not supported on tvOS
- Audio-routing category options (not applicable to an Apple TV).

See `PORTING_REPORT.md` for the port detail and checklist.
