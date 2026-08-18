// Copyright 2021 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';

import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const AnalyticsExampleApp());
}

class AnalyticsExampleApp extends StatelessWidget {
  const AnalyticsExampleApp({super.key});

  @override
  Widget build(BuildContext context) {
    final analytics = FirebaseAnalytics.instance;
    return MaterialApp(
      title: 'firebase_analytics tvOS example',
      theme: ThemeData.dark(useMaterial3: true),
      // The FirebaseAnalyticsObserver logs screen_view events automatically.
      navigatorObservers: [
        FirebaseAnalyticsObserver(analytics: analytics),
      ],
      home: AnalyticsHomePage(analytics: analytics),
    );
  }
}

class AnalyticsHomePage extends StatefulWidget {
  const AnalyticsHomePage({super.key, required this.analytics});

  final FirebaseAnalytics analytics;

  @override
  State<AnalyticsHomePage> createState() => _AnalyticsHomePageState();
}

class _AnalyticsHomePageState extends State<AnalyticsHomePage> {
  String _status = 'Ready. Pick an action with the Siri Remote.';

  Future<void> _run(String label, Future<void> Function() action) async {
    try {
      await action();
      setState(() => _status = '✅ $label — sent to Firebase.');
    } catch (e) {
      setState(() => _status = '❌ $label — $e');
    }
  }

  @override
  void initState() {
    super.initState();
    // Make sure collection is on (it is by default unless disabled remotely).
    widget.analytics.setAnalyticsCollectionEnabled(true);
  }

  @override
  Widget build(BuildContext context) {
    final a = widget.analytics;
    return Scaffold(
      appBar: AppBar(title: const Text('firebase_analytics · tvOS')),
      body: Padding(
        padding: const EdgeInsets.all(48),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(_status, style: const TextStyle(fontSize: 28)),
            const SizedBox(height: 32),
            Wrap(
              spacing: 24,
              runSpacing: 24,
              children: [
                ElevatedButton(
                  autofocus: true,
                  onPressed: () => _run(
                    'logEvent(test_event)',
                    () => a.logEvent(
                      name: 'test_event',
                      parameters: <String, Object>{
                        'source': 'apple_tv',
                        'string': 'hello_tvos',
                        'int': 42,
                      },
                    ),
                  ),
                  child: const Text('logEvent: test_event'),
                ),
                ElevatedButton(
                  onPressed: () => _run(
                    'logLogin',
                    () => a.logLogin(loginMethod: 'demo'),
                  ),
                  child: const Text('logLogin'),
                ),
                ElevatedButton(
                  onPressed: () => _run(
                    'logScreenView',
                    () => a.logScreenView(screenName: 'Home_tvOS'),
                  ),
                  child: const Text('logScreenView'),
                ),
                ElevatedButton(
                  onPressed: () => _run(
                    'setUserProperty',
                    () => a.setUserProperty(name: 'tier', value: 'demo'),
                  ),
                  child: const Text('setUserProperty'),
                ),
                ElevatedButton(
                  onPressed: () => _run(
                    'getAppInstanceId',
                    () async {
                      final id = await a.appInstanceId;
                      setState(() => _status = 'appInstanceId = $id');
                    },
                  ),
                  child: const Text('getAppInstanceId'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
