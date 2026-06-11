# audioplayers_tvos

tvOS implementation of [`audioplayers`](https://pub.dev/packages/audioplayers)
for [flutter-tvos](https://github.com/fluttertv/flutter-tvos)
(port of `audioplayers_darwin`, hand-finished for tvOS).

## Usage

```yaml
dependencies:
  audioplayers: ^6.x
  audioplayers_tvos: ^0.0.2
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

## Dependency management

Supports both **Swift Package Manager** and **CocoaPods** from a single
source tree. `flutter-tvos` wires the right one automatically: apps on
Flutter 3.44+ link it via SwiftPM (this package ships a `tvos/Package.swift`),
while CocoaPods-based projects keep using the podspec. No manual setup needed.
