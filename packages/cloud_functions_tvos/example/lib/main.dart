// Copyright 2019 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import 'package:cloud_functions/cloud_functions.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';

import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(const FunctionsExampleApp());
}

class FunctionsExampleApp extends StatelessWidget {
  const FunctionsExampleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'cloud_functions tvOS example',
      theme: ThemeData.dark(useMaterial3: true),
      home: const FunctionsHomePage(),
    );
  }
}

class FunctionsHomePage extends StatefulWidget {
  const FunctionsHomePage({super.key});

  @override
  State<FunctionsHomePage> createState() => _FunctionsHomePageState();
}

class _FunctionsHomePageState extends State<FunctionsHomePage> {
  String _status = 'Ready — call a callable function with the Siri Remote.';

  Future<void> _callFunction() async {
    setState(() => _status = 'calling…');
    try {
      // Replace 'listFruit' with a callable you have deployed to your project.
      final callable = FirebaseFunctions.instance.httpsCallable('listFruit');
      final result = await callable.call<dynamic>();
      setState(() => _status = '✅ result: ${result.data}');
    } on FirebaseFunctionsException catch (e) {
      // Reaching the backend (even an error) proves the plugin works on tvOS.
      setState(() => _status = '⚠️ FunctionsException [${e.code}]: ${e.message}');
    } catch (e) {
      setState(() => _status = '❌ $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('cloud_functions · tvOS')),
      body: Padding(
        padding: const EdgeInsets.all(48),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(_status, style: const TextStyle(fontSize: 26)),
            const SizedBox(height: 32),
            ElevatedButton(
              autofocus: true,
              onPressed: _callFunction,
              child: const Text('call httpsCallable("listFruit")'),
            ),
          ],
        ),
      ),
    );
  }
}
