// Copyright 2019 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_remote_config/firebase_remote_config.dart';
import 'package:flutter/material.dart';

import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(const RemoteConfigExampleApp());
}

class RemoteConfigExampleApp extends StatelessWidget {
  const RemoteConfigExampleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'firebase_remote_config tvOS example',
      theme: ThemeData.dark(useMaterial3: true),
      home: const RemoteConfigHomePage(),
    );
  }
}

class RemoteConfigHomePage extends StatefulWidget {
  const RemoteConfigHomePage({super.key});

  @override
  State<RemoteConfigHomePage> createState() => _RemoteConfigHomePageState();
}

class _RemoteConfigHomePageState extends State<RemoteConfigHomePage> {
  final _rc = FirebaseRemoteConfig.instance;
  String _status = 'Ready.';
  String _welcome = '(not fetched yet)';

  @override
  void initState() {
    super.initState();
    _rc.setDefaults(const {
      'welcome_message': 'Hello from tvOS defaults',
      'feature_enabled': false,
    });
  }

  Future<void> _run(String label, Future<void> Function() action) async {
    try {
      await action();
      setState(() => _status = '✅ $label — ok.');
    } catch (e) {
      setState(() => _status = '❌ $label — $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('firebase_remote_config · tvOS')),
      body: Padding(
        padding: const EdgeInsets.all(48),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(_status, style: const TextStyle(fontSize: 28)),
            const SizedBox(height: 16),
            Text(
              'welcome_message = $_welcome',
              style: const TextStyle(fontSize: 24),
            ),
            const SizedBox(height: 32),
            Wrap(
              spacing: 24,
              runSpacing: 24,
              children: [
                ElevatedButton(
                  autofocus: true,
                  onPressed: () => _run('fetchAndActivate', () async {
                    await _rc.setConfigSettings(
                      RemoteConfigSettings(
                        fetchTimeout: const Duration(seconds: 10),
                        minimumFetchInterval: Duration.zero,
                      ),
                    );
                    final activated = await _rc.fetchAndActivate();
                    setState(() {
                      _welcome = _rc.getString('welcome_message');
                      _status = '✅ fetchAndActivate — activated=$activated';
                    });
                  }),
                  child: const Text('fetch & activate'),
                ),
                ElevatedButton(
                  onPressed: () => _run('read defaults', () async {
                    setState(() {
                      _welcome = _rc.getString('welcome_message');
                    });
                  }),
                  child: const Text('read current value'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
