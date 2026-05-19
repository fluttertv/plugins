import MediaPlayer

#if (os(iOS) || os(tvOS))
  struct AudioContext {
    let category: AVAudioSession.Category
    let options: [AVAudioSession.CategoryOptions]

    init() {
      self.category = .playback
      self.options = []
    }

    init(
      category: AVAudioSession.Category,
      options: [AVAudioSession.CategoryOptions]
    ) {
      self.category = category
      self.options = options
    }

    public func activateAudioSession(
      active: Bool
    ) throws {
      let session = AVAudioSession.sharedInstance()
      try session.setActive(active)
    }

    public func apply() throws {
      let session = AVAudioSession.sharedInstance()
      let combinedOptions = options.reduce(AVAudioSession.CategoryOptions()) {
        [$0, $1]
      }
      try session.setCategory(category, options: combinedOptions)
    }

    public static func parse(args: [String: Any]) throws -> AudioContext? {
      guard let categoryString = args["category"] as! String? else {
        throw AudioPlayerError.error("Null value received for category")
      }
      guard let category = try parseCategory(category: categoryString) else {
        return nil
      }

      guard let optionStrings = args["options"] as! [String]? else {
        throw AudioPlayerError.error("Null value received for options")
      }
      let options = try optionStrings.compactMap {
        try parseCategoryOption(option: $0)
      }
      if optionStrings.count != options.count {
        return nil
      }

      return AudioContext(
        category: category,
        options: options
      )
    }

    private static func parseCategory(category: String) throws -> AVAudioSession.Category? {
      switch category {
      case "ambient":
        return .ambient
      case "soloAmbient":
        return .soloAmbient
      case "playback":
        return .playback
      case "record":
        return .record
      case "playAndRecord":
        return .playAndRecord
      case "multiRoute":
        return .multiRoute
      default:
        throw AudioPlayerError.error("Invalid Category \(category)")
      }
    }

    private static func parseCategoryOption(option: String) throws -> AVAudioSession
      .CategoryOptions?
    {
      switch option {
      case "mixWithOthers":
        return .mixWithOthers
      case "duckOthers":
        return .duckOthers
      // tvOS routes audio over HDMI/eARC/AirPlay and has no Bluetooth /
      // speaker routing options. These map to nil on tvOS (playback is
      // unaffected — the default route is used).
      case "allowBluetooth":
        #if os(tvOS)
          return nil
        #else
          return .allowBluetooth
        #endif
      case "defaultToSpeaker":
        #if os(tvOS)
          return nil
        #else
          return .defaultToSpeaker
        #endif
      case "interruptSpokenAudioAndMixWithOthers":
        return .interruptSpokenAudioAndMixWithOthers
      case "allowBluetoothA2DP":
        #if os(tvOS)
          return nil
        #else
          if #available(iOS 10.0, *) {
            return .allowBluetoothA2DP
          } else {
            throw AudioPlayerError.warning(
              "Category Option allowBluetoothA2DP is only available on iOS 10+")
          }
        #endif
      case "allowAirPlay":
        if #available(iOS 10.0, tvOS 10.0, *) {
          return .allowAirPlay
        } else {
          throw AudioPlayerError.warning(
            "Category Option allowAirPlay is only available on iOS 10+")
        }
      case "overrideMutedMicrophoneInterruption":
        // tvOS has no microphone, so this AVAudioSession option does not
        // exist there. Maps to nil (no effect) — playback is unaffected.
        #if os(tvOS)
          return nil
        #else
          if #available(iOS 14.5, *) {
            return .overrideMutedMicrophoneInterruption
          } else {
            throw AudioPlayerError.warning(
              "Category Option overrideMutedMicrophoneInterruption is only available on iOS 14.5+")
          }
        #endif
      default:
        throw AudioPlayerError.error("Invalid Category Option \(option)")
      }
    }
  }
#else
  // no-op impl of AudioContext for macos
  struct AudioContext {
    func activateAudioSession(active: Bool) throws {
    }

    func apply() throws {
      throw AudioPlayerError.warning("AudioContext configuration is not available on macOS")
    }

    static func parse(args: [String: Any]) throws -> AudioContext? {
      return AudioContext()
    }
  }
#endif
