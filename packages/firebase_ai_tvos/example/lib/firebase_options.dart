// PLACEHOLDER — replace by running `flutterfire configure` in this example dir.
// On tvOS, defaultTargetPlatform == TargetPlatform.iOS, so the `ios` entry is
// what Apple TV uses (your iOS Firebase app config is reused for tvOS).
// ignore_for_file: lines_longer_than_80_chars
import 'package:firebase_core/firebase_core.dart' show FirebaseOptions;
import 'package:flutter/foundation.dart'
    show defaultTargetPlatform, kIsWeb, TargetPlatform;

class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      throw UnsupportedError('This example targets Apple TV (tvOS) only.');
    }
    switch (defaultTargetPlatform) {
      case TargetPlatform.iOS: // tvOS reports iOS
        return ios;
      default:
        throw UnsupportedError('This example targets Apple TV (tvOS) only.');
    }
  }

  // Replace with your real values — run `flutterfire configure`, or copy them
  // from your iOS app's GoogleService-Info.plist / Firebase console.
  static const FirebaseOptions ios = FirebaseOptions(
    apiKey: 'REPLACE_ME',
    appId: 'REPLACE_ME', // GOOGLE_APP_ID
    messagingSenderId: 'REPLACE_ME', // GCM_SENDER_ID
    projectId: 'REPLACE_ME',
    storageBucket: 'REPLACE_ME',
    iosBundleId: 'com.example.firebaseAiExample',
  );
}
