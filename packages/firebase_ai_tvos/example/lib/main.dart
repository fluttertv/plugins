// Copyright 2026 Google LLC. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE file.

import 'package:firebase_ai/firebase_ai.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';

import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(const AiExampleApp());
}

class AiExampleApp extends StatelessWidget {
  const AiExampleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'firebase_ai tvOS example',
      theme: ThemeData.dark(useMaterial3: true),
      home: const AiHomePage(),
    );
  }
}

class AiHomePage extends StatefulWidget {
  const AiHomePage({super.key});

  @override
  State<AiHomePage> createState() => _AiHomePageState();
}

class _AiHomePageState extends State<AiHomePage> {
  String _status = 'Ready — ask Gemini with the Siri Remote.';

  Future<void> _ask() async {
    setState(() => _status = 'thinking…');
    try {
      final model =
          FirebaseAI.googleAI().generativeModel(model: 'gemini-flash-latest');
      final response = await model.generateContent([
        Content.text('In one short sentence, what is Apple TV?'),
      ]);
      setState(() => _status = '✅ ${response.text ?? "(no text)"}');
    } catch (e) {
      // Reaching the AI backend (even an error) proves the plugin works on tvOS.
      setState(() => _status = '⚠️ $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('firebase_ai · tvOS')),
      body: Padding(
        padding: const EdgeInsets.all(48),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(_status, style: const TextStyle(fontSize: 24)),
            const SizedBox(height: 32),
            ElevatedButton(
              autofocus: true,
              onPressed: _ask,
              child: const Text('generateContent (Gemini)'),
            ),
          ],
        ),
      ),
    );
  }
}
