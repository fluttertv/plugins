// Copyright 2026 The FlutterTV Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

/// tvOS (Apple TV) implementation of `flutter_tts`.
///
/// This package is native-only: the Swift / ObjC `FlutterTtsPlugin`
/// (see `tvos/Classes/`) is auto-registered for the `tvos` platform via
/// `pluginClass` in `pubspec.yaml` and answers the same method channel
/// (`flutter_tts`) that the upstream `flutter_tts` Dart package talks
/// to. Consumers therefore use the upstream
/// `package:flutter_tts/flutter_tts.dart` API directly — nothing from
/// this library is imported at runtime on tvOS.
///
/// This file exists so the package has a public Dart entry point and is
/// safe to depend on / publish.
library flutter_tts_tvos;
