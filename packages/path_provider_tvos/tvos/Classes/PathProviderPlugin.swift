// Copyright 2026 The FlutterTV Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// Maintained tvOS implementation of `path_provider`.
//
// tvOS has a normal app sandbox (Documents, Library, Library/Caches,
// Library/Application Support) plus NSTemporaryDirectory(), so the
// standard NSSearchPath* lookups path_provider_foundation uses on iOS
// work unchanged here. There is no user-facing Downloads directory on
// tvOS, so that request returns nil (matching iOS/path_provider, where
// downloads is macOS-only).

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

  /// Application Support / Caches are not guaranteed to exist on first
  /// launch; create them so callers can write immediately (this mirrors
  /// path_provider_foundation's behaviour on iOS/macOS).
  private func ensuredDirectory(
    _ type: FileManager.SearchPathDirectory
  ) -> String? {
    guard let path = directory(type) else { return nil }
    if !FileManager.default.fileExists(atPath: path) {
      try? FileManager.default.createDirectory(
        atPath: path, withIntermediateDirectories: true, attributes: nil)
    }
    return path
  }
}
