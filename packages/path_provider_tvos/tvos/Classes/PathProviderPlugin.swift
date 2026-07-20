// Copyright 2026 The FlutterTV Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// Maintained tvOS implementation of `path_provider`.
//
// The tvOS sandbox is NOT the iOS sandbox. Measured on a physical Apple TV 4K
// (tvOS 26.5) by writing a file into each directory:
//
//   tmp                          writable
//   Library/Caches               writable
//   Documents                    exists, but writes are DENIED (errno 1)
//   Library/Application Support  does not exist and CANNOT be created (errno 1)
//
// Only Caches and tmp are usable for writing. tvOS provides no persistent
// local storage by platform contract — data that must survive belongs on a
// server or in iCloud key-value storage, and even Caches is purgeable at any
// time. The tvOS *simulator* permits all of these writes, so this difference
// appears only on real hardware.
//
// Documents is still returned: it is a real directory and reads work. Callers
// simply must not write there. Application Support returns nil instead of a
// path that neither exists nor can be created — path_provider turns nil into
// MissingPlatformDirectoryException at the call site, which is far easier to
// diagnose than an errno at the caller's first write.
//
// There is no user-facing Downloads directory on tvOS, so that request returns
// nil (matching iOS/path_provider, where downloads is macOS-only).

import Flutter
import Foundation

public class PathProviderPlugin: NSObject, FlutterPlugin {
  public static func register(with registrar: FlutterPluginRegistrar) {
    let channel = FlutterMethodChannel(
      name: "plugins.flutter.io/path_provider",
      binaryMessenger: registrar.messenger())
    registrar.addMethodCallDelegate(PathProviderPlugin(), channel: channel)
  }

  public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
    switch call.method {
    case "getTemporaryDirectory":
      result(NSTemporaryDirectory())
    case "getApplicationDocumentsDirectory":
      // Returned for parity with iOS, but NOT writable on tvOS — see above.
      result(directory(.documentDirectory))
    case "getApplicationSupportDirectory":
      result(ensuredDirectory(.applicationSupportDirectory))
    case "getApplicationCacheDirectory":
      result(ensuredDirectory(.cachesDirectory))
    case "getLibraryDirectory":
      result(directory(.libraryDirectory))
    case "getDownloadsDirectory":
      // No user Downloads directory in the tvOS sandbox.
      result(nil)
    default:
      result(FlutterMethodNotImplemented)
    }
  }

  private func directory(_ type: FileManager.SearchPathDirectory) -> String? {
    return NSSearchPathForDirectoriesInDomains(type, .userDomainMask, true)
      .first
  }

  /// Application Support / Caches are not guaranteed to exist on first launch,
  /// so create them when missing (mirroring path_provider_foundation on
  /// iOS/macOS). On tvOS the creation genuinely fails for Application Support,
  /// so the error is surfaced rather than swallowed: `try?` here would return a
  /// path that does not exist, and the caller would only find out at its first
  /// write, with an errno that names nothing useful.
  private func ensuredDirectory(
    _ type: FileManager.SearchPathDirectory
  ) -> String? {
    guard let path = directory(type) else { return nil }
    if !FileManager.default.fileExists(atPath: path) {
      do {
        try FileManager.default.createDirectory(
          atPath: path, withIntermediateDirectories: true, attributes: nil)
      } catch {
        NSLog(
          "[path_provider_tvos] cannot create \(path): "
            + "\(error.localizedDescription). The tvOS sandbox only permits "
            + "writes to Library/Caches and tmp.")
        return nil
      }
    }
    return path
  }
}
