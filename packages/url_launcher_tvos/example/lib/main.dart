// Copyright 2013 The Flutter Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// ignore_for_file: public_member_api_docs

import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

void main() {
  runApp(const UrlLauncherTvosApp());
}

class UrlLauncherTvosApp extends StatelessWidget {
  const UrlLauncherTvosApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'url_launcher tvOS example',
      theme: ThemeData.dark(useMaterial3: true),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  // tvOS has no in-app browser, so only external launches do anything: an app
  // URL scheme (or universal link) that another installed app can handle. This
  // example registers `ullauncherdemo://` for itself in tvos/Runner/Info.plist,
  // so the launch below actually hands off. A plain web URL has nothing to open.
  static final Uri _appScheme = Uri.parse('ullauncherdemo://demo');
  static final Uri _webUrl = Uri.parse('https://flutter.dev');

  String _status = 'Pick an action with the Siri Remote.';

  Future<void> _canLaunch(Uri url) async {
    final bool can = await canLaunchUrl(url);
    setState(() => _status = 'canLaunchUrl($url) = $can');
  }

  Future<void> _launchExternal(Uri url) async {
    try {
      final bool ok = await launchUrl(url, mode: LaunchMode.externalApplication);
      setState(() => _status = 'launchUrl($url) = $ok');
    } catch (e) {
      setState(() => _status = '$url threw: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('url_launcher · tvOS')),
      body: Padding(
        padding: const EdgeInsets.all(48),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            Text(_status, style: const TextStyle(fontSize: 24)),
            const SizedBox(height: 12),
            const Text(
              'In-app browser modes are unsupported on tvOS (no SafariServices).',
              style: TextStyle(fontSize: 18, color: Colors.white70),
            ),
            const SizedBox(height: 32),
            ElevatedButton(
              autofocus: true,
              onPressed: () => _launchExternal(_appScheme),
              child: const Text('Launch app scheme (ullauncherdemo://)'),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => _launchExternal(_webUrl),
              child: const Text('Launch web URL (no browser → false)'),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => _canLaunch(_appScheme),
              child: const Text('canLaunchUrl (app scheme)'),
            ),
          ],
        ),
      ),
    );
  }
}
