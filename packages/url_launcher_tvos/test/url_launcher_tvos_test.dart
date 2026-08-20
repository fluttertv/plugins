// Copyright 2026 The FlutterTV Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// Generated on 2026-08-19 by `flutter-tvos plugin port`.
// Source plugin: url_launcher_ios

import 'package:flutter_test/flutter_test.dart';
import 'package:url_launcher_platform_interface/url_launcher_platform_interface.dart';
import 'package:url_launcher_tvos/url_launcher_tvos.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('registerWith installs UrlLauncherTvos as the platform instance', () {
    UrlLauncherTvos.registerWith();
    expect(UrlLauncherPlatform.instance, isA<UrlLauncherTvos>());
  });

  group('supportsMode — tvOS has no in-app browser', () {
    final UrlLauncherTvos launcher = UrlLauncherTvos();

    test('external modes are supported', () async {
      expect(
        await launcher.supportsMode(PreferredLaunchMode.externalApplication),
        isTrue,
      );
      expect(
        await launcher.supportsMode(
          PreferredLaunchMode.externalNonBrowserApplication,
        ),
        isTrue,
      );
      expect(
        await launcher.supportsMode(PreferredLaunchMode.platformDefault),
        isTrue,
      );
    });

    test('in-app browser modes are NOT supported (unlike iOS)', () async {
      expect(
        await launcher.supportsMode(PreferredLaunchMode.inAppBrowserView),
        isFalse,
      );
      expect(
        await launcher.supportsMode(PreferredLaunchMode.inAppWebView),
        isFalse,
      );
    });

    test('nothing supports close, since there is no in-app browser', () async {
      expect(
        await launcher.supportsCloseForMode(
          PreferredLaunchMode.inAppBrowserView,
        ),
        isFalse,
      );
    });
  });
}
