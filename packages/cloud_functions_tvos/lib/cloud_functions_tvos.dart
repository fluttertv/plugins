// Copyright 2019, the Chromium project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// cloud_functions's public Dart API (FirebaseFunctions, HttpsCallable, …) has
// no per-platform Dart override — it talks to native through
// cloud_functions_platform_interface's MethodChannel implementation regardless
// of platform. Duplicating those classes here would create incompatible types
// vs. apps that import package:cloud_functions/cloud_functions.dart directly.
// This package only supplies the native tvOS pluginClass (tvos/Classes/); apps
// depend on cloud_functions (Dart API) and cloud_functions_tvos (native
// registration) side by side — see example/.
export 'package:cloud_functions/cloud_functions.dart';
