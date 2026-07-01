// Copyright 2020, the Chromium project authors.  Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

// Same reasoning as firebase_core_tvos: cloud_firestore's public Dart API
// (FirebaseFirestore, Query, DocumentSnapshot, …) has no per-platform Dart
// override — it talks to native through cloud_firestore_platform_interface's
// MethodChannel implementation regardless of platform. Duplicating it here
// would create incompatible types vs. apps that import
// package:cloud_firestore/cloud_firestore.dart directly. This package only
// supplies the native tvOS pluginClass (tvos/Classes/); apps depend on
// cloud_firestore (Dart API) and cloud_firestore_tvos (native registration)
// side by side — see example/.
export 'package:cloud_firestore/cloud_firestore.dart';
