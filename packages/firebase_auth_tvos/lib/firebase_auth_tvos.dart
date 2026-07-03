// Copyright 2019 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Same reasoning as firebase_core_tvos: firebase_auth's public Dart API
// (FirebaseAuth, User, UserCredential, …) has no per-platform Dart
// override — it talks to native through firebase_auth_platform_interface's
// MethodChannel implementation regardless of platform. Duplicating it here
// would create incompatible types vs. apps that import
// package:firebase_auth/firebase_auth.dart directly. This package only
// supplies the native tvOS pluginClass (tvos/Classes/); apps depend on
// firebase_auth (Dart API) and firebase_auth_tvos (native registration)
// side by side — see example/.
export 'package:firebase_auth/firebase_auth.dart';
