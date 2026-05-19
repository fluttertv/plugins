# flutter_tts_tvos

tvOS implementation of [`flutter_tts`](https://pub.dev/packages/flutter_tts)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos)
(hand-finished for tvOS).

> **Verified:** simulator build GREEN. On-device pass recommended.

## Usage

```yaml
dependencies:
  flutter_tts: ^4.x
  flutter_tts_tvos:
    path: ../flutter_tts_tvos   # or pub.dev once published
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
