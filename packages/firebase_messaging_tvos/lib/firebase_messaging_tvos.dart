// Copyright 2020 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Same reasoning as firebase_core_tvos: firebase_messaging's public Dart
// API (FirebaseMessaging, RemoteMessage, …) has no per-platform Dart
// override — it talks to native through firebase_messaging_platform_interface's
// MethodChannel implementation regardless of platform. Duplicating it here
// would create incompatible types vs. apps that import
// package:firebase_messaging/firebase_messaging.dart directly. This package
// only supplies the native tvOS pluginClass (tvos/Classes/); apps depend on
// firebase_messaging (Dart API) and firebase_messaging_tvos (native
// registration) side by side — see example/.
export 'package:firebase_messaging/firebase_messaging.dart';
