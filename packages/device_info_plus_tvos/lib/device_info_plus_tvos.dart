// Copyright 2026 The FlutterTV Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// tvOS (Apple TV) implementation of `device_info_plus`.
//
// This package is native-only: the Swift `FPPDeviceInfoPlusPlugin`
// (see `tvos/Classes/`) is auto-registered for the `tvos` platform via
// `pluginClass` in `pubspec.yaml` and answers the same method channel
// (`dev.fluttercommunity.plus/device_info`) that
// `device_info_plus_platform_interface`'s default
// `MethodChannelDeviceInfoPlus` already talks to. Consumers therefore
// use the upstream `package:device_info_plus/device_info_plus.dart`
// API directly — on tvOS, `deviceInfo` resolves to `IosDeviceInfo`
// (UIDevice-backed; tvOS reports `systemName == "tvOS"`).
//
// This file exists so the package has a public Dart entry point and is
// safe to depend on / publish.
library device_info_plus_tvos;
