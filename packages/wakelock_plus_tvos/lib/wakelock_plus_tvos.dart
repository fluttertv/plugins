// Copyright 2026 The FlutterTV Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// tvOS (Apple TV) implementation of `wakelock_plus`.
//
// This package is native-only: the Swift `WakelockPlusPlugin`
// (see `tvos/Classes/`) is auto-registered for the `tvos` platform via
// `pluginClass` in `pubspec.yaml` and answers the same method channel
// (`dev.fluttercommunity.plus/wakelock`) that
// `wakelock_plus_platform_interface`'s default Pigeon implementation
// already talks to. Consumers therefore use the upstream
// `package:wakelock_plus/wakelock_plus.dart` API directly — nothing
// from this library is imported at runtime.
//
// This file exists so the package has a public Dart entry point and is
// safe to depend on / publish.
library wakelock_plus_tvos;
