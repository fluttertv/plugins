# firebase_ai_tvos example (Apple TV)

Minimal app that calls a Gemini generative model via **Firebase AI Logic** from
tvOS, to verify the `firebase_ai_tvos` plugin on the Simulator and a physical
Apple TV.

## 1. Connect it to Firebase
On tvOS, `defaultTargetPlatform == TargetPlatform.iOS`, so the iOS Firebase app
config is used. Run `flutterfire configure` (pick your project → the iOS app),
and enable the **Firebase AI Logic** API + Gemini in the console.

## 2. Run it
```bash
export PATH="/path/to/flutter-tvos/bin:$PATH"
flutter-tvos pub get
flutter-tvos run -d "Apple TV"     # simulator, or a physical Apple TV
```
Press **generateContent (Gemini)** with the Siri Remote. A returned sentence (or
even a backend error) confirms the request reached Firebase AI from Apple TV.
