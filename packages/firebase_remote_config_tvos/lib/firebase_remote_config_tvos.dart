// Copyright 2019 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// firebase_remote_config's public Dart API (FirebaseRemoteConfig,
// RemoteConfigValue, RemoteConfigSettings, …) has no per-platform Dart
// override — it talks to native through
// firebase_remote_config_platform_interface's MethodChannel implementation
// regardless of platform. Duplicating those classes here would create
// incompatible types vs. apps that import
// package:firebase_remote_config/firebase_remote_config.dart directly. This
// package only supplies the native tvOS pluginClass (tvos/Classes/); apps
// depend on firebase_remote_config (Dart API) and firebase_remote_config_tvos
// (native registration) side by side — see example/.
export 'package:firebase_remote_config/firebase_remote_config.dart';
