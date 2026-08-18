// Copyright 2021 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// firebase_analytics's public Dart API (FirebaseAnalytics, the navigator
// observer, AnalyticsCallOptions, …) has no per-platform Dart override — it
// talks to native through firebase_analytics_platform_interface's
// MethodChannel implementation regardless of platform. Duplicating those
// classes here would create incompatible types vs. apps that import
// package:firebase_analytics/firebase_analytics.dart directly. This package
// only supplies the native tvOS pluginClass (tvos/Classes/); apps depend on
// firebase_analytics (Dart API) and firebase_analytics_tvos (native
// registration) side by side — see example/.
export 'package:firebase_analytics/firebase_analytics.dart';
