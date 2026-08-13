// Copyright 2019 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// firebase_app_check's public Dart API (FirebaseAppCheck, provider enums, …)
// has no per-platform Dart override — it talks to native through
// firebase_app_check_platform_interface's MethodChannel implementation
// regardless of platform. Duplicating those classes here would create
// incompatible types vs. apps that import
// package:firebase_app_check/firebase_app_check.dart directly. This package
// only supplies the native tvOS pluginClass (tvos/Classes/); apps depend on
// firebase_app_check (Dart API) and firebase_app_check_tvos (native
// registration) side by side — see example/.
export 'package:firebase_app_check/firebase_app_check.dart';
