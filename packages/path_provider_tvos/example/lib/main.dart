import 'package:flutter/material.dart';

void main() => runApp(const ExampleApp());

class ExampleApp extends StatelessWidget {
  const ExampleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('path_provider_tvos')),
        body: const Center(
          child: Text(
            'Native federated tvOS skeleton.\n'
            'Implement the plugin (see PORTING_REPORT.md), then call it here.',
            textAlign: TextAlign.center,
          ),
        ),
      ),
    );
  }
}
