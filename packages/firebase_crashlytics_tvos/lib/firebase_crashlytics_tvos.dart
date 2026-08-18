// Copyright 2019 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// firebase_crashlytics's public Dart API (FirebaseCrashlytics, …) has no
// per-platform Dart override — it talks to native through
// firebase_crashlytics_platform_interface's MethodChannel implementation
// regardless of platform. Duplicating those classes here would create
// incompatible types vs. apps that import
// package:firebase_crashlytics/firebase_crashlytics.dart directly. This package
// only supplies the native tvOS pluginClass (tvos/Classes/); apps depend on
// firebase_crashlytics (Dart API) and firebase_crashlytics_tvos (native
// registration) side by side — see example/.
export 'package:firebase_crashlytics/firebase_crashlytics.dart';
