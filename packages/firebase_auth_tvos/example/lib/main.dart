// Copyright 2026 fluttertv. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Trimmed down by hand from upstream firebase_auth's example app, which
// pulls in several third-party social-sign-in UI packages
// (flutter_facebook_auth, google_sign_in, font_awesome_flutter, …) that
// have no tvOS implementation and, separately, were incompatible with this
// monorepo's pinned Flutter SDK (font_awesome_flutter 10.x extends the now
// `final` IconData class). None of those providers work on tvOS anyway —
// they rely on browser-redirect flows (ASWebAuthenticationSession /
// SFSafariViewController) that tvOS doesn't support. This example instead
// exercises the auth flows that are tvOS-compatible: anonymous and
// email/password sign-in, both of which go straight to the Identity
// Toolkit REST API with no browser involved.

import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'firebase_options.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  Future<FirebaseAuth> _auth() async {
    final app = await Firebase.initializeApp(
      options: DefaultFirebaseOptions.currentPlatform,
    );
    return FirebaseAuth.instanceFor(app: app);
  }

  Future<void> signInAnonymously() async {
    final auth = await _auth();
    final credential = await auth.signInAnonymously();
    print('Signed in anonymously as ${credential.user?.uid}');
  }

  Future<void> createUser() async {
    final auth = await _auth();
    final credential = await auth.createUserWithEmailAndPassword(
      email: 'demo@example.com',
      password: 'correct horse battery staple',
    );
    print('Created user ${credential.user?.uid}');
  }

  Future<void> signOut() async {
    final auth = await _auth();
    await auth.signOut();
    print('Signed out');
  }

  void authStateChanges() async {
    final auth = await _auth();
    auth.authStateChanges().listen((user) {
      print('Auth state changed: ${user?.uid}');
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('Firebase Auth example app')),
        body: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              ElevatedButton(
                onPressed: signInAnonymously,
                child: const Text('Sign in anonymously'),
              ),
              ElevatedButton(
                onPressed: createUser,
                child: const Text('Create email/password user'),
              ),
              ElevatedButton(
                onPressed: authStateChanges,
                child: const Text('Listen for auth state changes'),
              ),
              ElevatedButton(
                onPressed: signOut,
                child: const Text('Sign out'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
