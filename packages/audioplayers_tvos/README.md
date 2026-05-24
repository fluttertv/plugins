# audioplayers_tvos

tvOS implementation of [`audioplayers`](https://pub.dev/packages/audioplayers)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos)
(port of `audioplayers_darwin`, hand-finished for tvOS).

> On-device verification recommended for audio-routing edge cases.

## Usage

```yaml
dependencies:
  audioplayers: ^6.x
  audioplayers_tvos: ^0.0.1
```

## tvOS support

### ✅ Supported
- Play / pause / stop / resume / seek / volume / playback rate /
  release; looping; asset, URL and byte sources (`AVPlayer` /
  `AVAudioPlayer`, available on tvOS).

### ⚠️ Limitations / differs from iOS
- `AVAudioSession` **category options that don't exist on tvOS** are
  accepted but have **no effect**: `allowBluetooth`,
  `allowBluetoothA2DP`, `defaultToSpeaker`,
  `overrideMutedMicrophoneInterruption`. An Apple TV routes audio over
  HDMI/eARC/AirPlay, so device-routing options are not applicable.

### ❌ Not supported on tvOS
- Bluetooth/earpiece/speaker audio routing controls (no such routes
  on tvOS); microphone-related options (no microphone).

See `PORTING_REPORT.md` for the port detail and checklist.
