// Copyright 2019 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_performance/firebase_performance.dart';
import 'package:flutter/material.dart';

import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const PerformanceExampleApp());
}

class PerformanceExampleApp extends StatelessWidget {
  const PerformanceExampleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'firebase_performance tvOS example',
      theme: ThemeData.dark(useMaterial3: true),
      home: const PerformanceHomePage(),
    );
  }
}

class PerformanceHomePage extends StatefulWidget {
  const PerformanceHomePage({super.key});

  @override
  State<PerformanceHomePage> createState() => _PerformanceHomePageState();
}

class _PerformanceHomePageState extends State<PerformanceHomePage> {
  final _perf = FirebasePerformance.instance;
  String _status = 'Ready. Traces/metrics upload to the Performance dashboard.';

  Future<void> _run(String label, Future<void> Function() action) async {
    try {
      await action();
      setState(() => _status = '✅ $label — sent.');
    } catch (e) {
      setState(() => _status = '❌ $label — $e');
    }
  }

  @override
  void initState() {
    super.initState();
    _perf.setPerformanceCollectionEnabled(true);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('firebase_performance · tvOS')),
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
                  onPressed: () => _run('custom trace', () async {
                    final trace = _perf.newTrace('tvos_test_trace');
                    await trace.start();
                    trace.putAttribute('source', 'apple_tv');
                    trace.incrementMetric('items', 3);
                    await Future<void>.delayed(
                        const Duration(milliseconds: 200));
                    await trace.stop();
                  }),
                  child: const Text('run custom trace'),
                ),
                ElevatedButton(
                  onPressed: () => _run('http metric', () async {
                    final metric = _perf.newHttpMetric(
                      'https://firebase.google.com',
                      HttpMethod.Get,
                    );
                    await metric.start();
                    metric.httpResponseCode = 200;
                    metric.responsePayloadSize = 1024;
                    await metric.stop();
                  }),
                  child: const Text('record HTTP metric'),
                ),
                ElevatedButton(
                  onPressed: () => _run('toggle collection', () async {
                    final on = await _perf.isPerformanceCollectionEnabled();
                    await _perf.setPerformanceCollectionEnabled(!on);
                    setState(() => _status = 'collection enabled = ${!on}');
                  }),
                  child: const Text('toggle collection'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
