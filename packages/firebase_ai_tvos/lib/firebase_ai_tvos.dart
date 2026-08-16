// Copyright 2026 Google LLC
// Use of this source code is governed by a BSD-style license.

// firebase_ai's public Dart API (FirebaseAI, GenerativeModel, chat, imagen, …)
// has no per-platform Dart override — the generative calls are HTTPS from Dart,
// and the sole native touch-point is a `getPlatformHeaders` method channel.
// Duplicating the Dart here would create incompatible types vs. apps importing
// package:firebase_ai/firebase_ai.dart directly. This package only supplies the
// native tvOS pluginClass (tvos/Classes/); apps depend on firebase_ai (Dart API)
// and firebase_ai_tvos (native registration) side by side — see example/.
export 'package:firebase_ai/firebase_ai.dart';
