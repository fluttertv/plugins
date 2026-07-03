// Copyright 2020 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// firebase_core's public Dart API (Firebase, FirebaseApp, FirebaseOptions, …)
// talks to the platform side purely through MethodChannelFirebase /
// MethodChannelFirebaseApp in firebase_core_platform_interface — there is no
// per-platform Dart override even on iOS. So this package only needs to
// supply the native tvOS pluginClass (see tvos/Classes/); duplicating the
// Dart API here would create a second, incompatible FirebaseApp type that
// firebase_auth_tvos / cloud_firestore_tvos and friends (which import
// package:firebase_core/firebase_core.dart directly) wouldn't recognize.
// Apps depend on firebase_core (for the Dart API) *and* firebase_core_tvos
// (for native plugin discovery/registration) side by side — see example/.
export 'package:firebase_core/firebase_core.dart';
