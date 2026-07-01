// Copyright 2020 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Same reasoning as firebase_core_tvos: firebase_storage's public Dart API
// (FirebaseStorage, Reference, UploadTask, …) has no per-platform Dart
// override — it talks to native through firebase_storage_platform_interface's
// MethodChannel implementation regardless of platform. Duplicating it here
// would create incompatible types vs. apps that import
// package:firebase_storage/firebase_storage.dart directly. This package
// only supplies the native tvOS pluginClass (tvos/Classes/); apps depend on
// firebase_storage (Dart API) and firebase_storage_tvos (native
// registration) side by side — see example/.
export 'package:firebase_storage/firebase_storage.dart';
