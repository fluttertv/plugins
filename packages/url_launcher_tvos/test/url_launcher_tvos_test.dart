// Copyright 2026 The FlutterTV Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
//
// Generated on 2026-08-19 by `flutter-tvos plugin port`.
// Source plugin: url_launcher_ios

import 'package:flutter/services.dart' show BinaryMessenger;
import 'package:flutter_test/flutter_test.dart';
import 'package:url_launcher_platform_interface/url_launcher_platform_interface.dart';
import 'package:url_launcher_tvos/src/messages.g.dart';
import 'package:url_launcher_tvos/url_launcher_tvos.dart';

/// A fake host API that records calls and returns canned results, so the tests
/// can assert *which* Pigeon channel a launch reaches without a real device.
class _FakeApi implements UrlLauncherApi {
  final List<String> calls = <String>[];
  LaunchResult canLaunchResult = LaunchResult.success;
  LaunchResult launchResult = LaunchResult.success;

  // Names are dictated by the generated Pigeon `UrlLauncherApi` interface.
  // ignore_for_file: non_constant_identifier_names
  @override
  BinaryMessenger? get pigeonVar_binaryMessenger => null;

  @override
  String get pigeonVar_messageChannelSuffix => '';

  @override
  Future<LaunchResult> canLaunchUrl(String url) async {
    calls.add('canLaunchUrl($url)');
    return canLaunchResult;
  }

  @override
  Future<LaunchResult> launchUrl(String url, bool universalLinksOnly) async {
    calls.add('launchUrl($url, universalLinksOnly: $universalLinksOnly)');
    return launchResult;
  }

  @override
  Future<InAppLoadResult> openUrlInSafariViewController(String url) async {
    calls.add('openUrlInSafariViewController($url)');
    return InAppLoadResult.noUI;
  }

  @override
  Future<void> closeSafariViewController() async {
    calls.add('closeSafariViewController()');
  }
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('registerWith installs UrlLauncherTvos as the platform instance', () {
    UrlLauncherTvos.registerWith();
    expect(UrlLauncherPlatform.instance, isA<UrlLauncherTvos>());
  });

  group('every launch mode uses the external channel (no in-app browser)', () {
    late _FakeApi api;
    late UrlLauncherTvos launcher;

    setUp(() {
      api = _FakeApi();
      launcher = UrlLauncherTvos(api: api);
    });

    test('externalApplication -> launchUrl channel', () async {
      await launcher.launchUrl(
        'https://example.com',
        const LaunchOptions(mode: PreferredLaunchMode.externalApplication),
      );
      expect(api.calls, <String>[
        'launchUrl(https://example.com, universalLinksOnly: false)',
      ]);
    });

    test('externalNonBrowserApplication -> universalLinksOnly = true', () async {
      await launcher.launchUrl(
        'https://example.com',
        const LaunchOptions(
          mode: PreferredLaunchMode.externalNonBrowserApplication,
        ),
      );
      expect(api.calls, <String>[
        'launchUrl(https://example.com, universalLinksOnly: true)',
      ]);
    });

    test('platformDefault falls back to external, never in-app', () async {
      await launcher.launchUrl(
        'https://example.com',
        const LaunchOptions(mode: PreferredLaunchMode.platformDefault),
      );
      expect(api.calls, <String>[
        'launchUrl(https://example.com, universalLinksOnly: false)',
      ]);
    });

    test('inAppBrowserView falls back to external, does NOT throw', () async {
      await launcher.launchUrl(
        'https://example.com',
        const LaunchOptions(mode: PreferredLaunchMode.inAppBrowserView),
      );
      // The in-app browser channel must NOT be reached on tvOS.
      expect(api.calls, isNot(contains('openUrlInSafariViewController(https://example.com)')));
      expect(api.calls, <String>[
        'launchUrl(https://example.com, universalLinksOnly: false)',
      ]);
    });

    test('inAppWebView falls back to external, does NOT throw', () async {
      await launcher.launchUrl(
        'https://example.com',
        const LaunchOptions(mode: PreferredLaunchMode.inAppWebView),
      );
      expect(api.calls, <String>[
        'launchUrl(https://example.com, universalLinksOnly: false)',
      ]);
    });

    // The regression the review flagged: the deprecated `launch()` infers
    // `useSafariVC` from the URL scheme, so a bare web URL used to route to the
    // in-app browser and throw. It must now launch externally.
    test('deprecated launch(webUrl) launches externally, does NOT throw',
        () async {
      final bool result = await launcher.launch(
        'https://example.com/help',
        useSafariVC: true, // what legacy_api.dart infers for an http(s) URL
        useWebView: false,
        enableJavaScript: false,
        enableDomStorage: false,
        universalLinksOnly: false,
        headers: const <String, String>{},
      );
      expect(result, isTrue);
      expect(api.calls, <String>[
        'launchUrl(https://example.com/help, universalLinksOnly: false)',
      ]);
    });

    test('an unclaimed URL returns false rather than throwing', () async {
      api.launchResult = LaunchResult.failure;
      final bool result = await launcher.launchUrl(
        'https://example.com',
        const LaunchOptions(mode: PreferredLaunchMode.inAppBrowserView),
      );
      expect(result, isFalse);
    });
  });

  group('capabilities — tvOS has no in-app browser', () {
    final UrlLauncherTvos launcher = UrlLauncherTvos(api: _FakeApi());

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
