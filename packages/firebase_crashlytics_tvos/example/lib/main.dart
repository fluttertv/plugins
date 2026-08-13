// Copyright 2020 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:flutter/material.dart';

import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  // Route uncaught Flutter framework errors to Crashlytics.
  FlutterError.onError =
      FirebaseCrashlytics.instance.recordFlutterFatalError;
  runApp(const CrashlyticsExampleApp());
}

class CrashlyticsExampleApp extends StatelessWidget {
  const CrashlyticsExampleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'firebase_crashlytics tvOS example',
      theme: ThemeData.dark(useMaterial3: true),
      home: const CrashlyticsHomePage(),
    );
  }
}

class CrashlyticsHomePage extends StatefulWidget {
  const CrashlyticsHomePage({super.key});

  @override
  State<CrashlyticsHomePage> createState() => _CrashlyticsHomePageState();
}

class _CrashlyticsHomePageState extends State<CrashlyticsHomePage> {
  final _crashlytics = FirebaseCrashlytics.instance;
  String _status = 'Ready. Crashlytics reports on the NEXT launch after a crash.';

  Future<void> _run(String label, Future<void> Function() action) async {
    try {
      await action();
      setState(() => _status = '✅ $label — sent to Crashlytics.');
    } catch (e) {
      setState(() => _status = '❌ $label — $e');
    }
  }

  @override
  void initState() {
    super.initState();
    _crashlytics.setCrashlyticsCollectionEnabled(true);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('firebase_crashlytics · tvOS')),
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
                    'recordError (non-fatal)',
                    () => _crashlytics.recordError(
                      Exception('tvOS non-fatal test error'),
                      StackTrace.current,
                      reason: 'apple_tv demo',
                    ),
                  ),
                  child: const Text('recordError (non-fatal)'),
                ),
                ElevatedButton(
                  onPressed: () => _run(
                    'log + setCustomKey',
                    () async {
                      await _crashlytics.setCustomKey('source', 'apple_tv');
                      await _crashlytics.log('tvOS crashlytics log line');
                    },
                  ),
                  child: const Text('log + custom key'),
                ),
                ElevatedButton(
                  onPressed: () => _run(
                    'setUserIdentifier',
                    () => _crashlytics.setUserIdentifier('tvos-demo-user'),
                  ),
                  child: const Text('setUserIdentifier'),
                ),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.red.shade700,
                  ),
                  // Forces a native crash. The report is uploaded on the NEXT
                  // launch — relaunch the app, then check the Crashlytics
                  // console.
                  onPressed: () => _crashlytics.crash(),
                  child: const Text('CRASH (test)'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
