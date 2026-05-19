import AVFoundation

// tvOS note: AVAudioSession exists on tvOS but its CategoryOptions are a
// narrow subset. Bluetooth/speaker routing options do not exist on tvOS
// (an Apple TV routes audio over HDMI/eARC/AirPlay), so those map to
// `nil` here — speech still plays through the default route. Mixing /
// ducking / AirPlay options are available on tvOS and kept.
enum AudioCategoryOptions: String {
  case iosAudioCategoryOptionsMixWithOthers
  case iosAudioCategoryOptionsDuckOthers
  case iosAudioCategoryOptionsInterruptSpokenAudioAndMixWithOthers
  case iosAudioCategoryOptionsAllowBluetooth
  case iosAudioCategoryOptionsAllowBluetoothA2DP
  case iosAudioCategoryOptionsAllowAirPlay
  case iosAudioCategoryOptionsDefaultToSpeaker

  func toAVAudioSessionCategoryOptions() -> AVAudioSession.CategoryOptions? {
    switch self {
    case .iosAudioCategoryOptionsMixWithOthers:
      return .mixWithOthers
    case .iosAudioCategoryOptionsDuckOthers:
      return .duckOthers
    case .iosAudioCategoryOptionsInterruptSpokenAudioAndMixWithOthers:
      return .interruptSpokenAudioAndMixWithOthers
    case .iosAudioCategoryOptionsAllowBluetooth:
      #if os(tvOS)
        return nil
      #else
        return .allowBluetooth
      #endif
    case .iosAudioCategoryOptionsAllowBluetoothA2DP:
      #if os(tvOS)
        return nil
      #else
        if #available(iOS 10.0, *) {
          return .allowBluetoothA2DP
        } else {
          return nil
        }
      #endif
    case .iosAudioCategoryOptionsAllowAirPlay:
      if #available(iOS 10.0, tvOS 10.0, *) {
        return .allowAirPlay
      } else {
        return nil
      }
    case .iosAudioCategoryOptionsDefaultToSpeaker:
      #if os(tvOS)
        return nil
      #else
        return .defaultToSpeaker
      #endif
    }
  }
}
