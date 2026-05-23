// Copyright 2026 The FlutterTV Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// tvOS (Apple TV) implementation of `package_info_plus`.
//
// This package is native-only: the Swift `FPPPackageInfoPlusPlugin`
// (see `tvos/Classes/`) is auto-registered for the `tvos` platform via
// `pluginClass` in `pubspec.yaml` and answers the same method channel
// (`dev.fluttercommunity.plus/package_info`) that
// `package_info_plus_platform_interface`'s default
// `MethodChannelPackageInfo` already talks to. Consumers therefore use
// the upstream `package:package_info_plus/package_info_plus.dart` API
// directly — nothing from this library is imported at runtime.
//
// This file exists so the package has a public Dart entry point and is
// safe to depend on / publish.
library package_info_plus_tvos;
