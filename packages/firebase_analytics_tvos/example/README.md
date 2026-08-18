# firebase_analytics_tvos example (Apple TV)

Minimal app that logs Firebase Analytics events from tvOS, for verifying the
`firebase_analytics_tvos` federated plugin on the Simulator and a physical
Apple TV.

## 1. Connect it to Firebase

On tvOS, `defaultTargetPlatform == TargetPlatform.iOS`, so **the iOS Firebase
app config is what tvOS uses** — you do _not_ need a separate tvOS app in the
Firebase console (though you may register one with the bundle id
`com.example.firebaseAnalyticsExample` if you prefer a clean split).

Two ways to supply the config:

**A. FlutterFire CLI (recommended — regenerates `lib/firebase_options.dart`):**

```bash
cd packages/firebase_analytics_tvos/example
flutterfire configure          # pick your project; select the iOS app
```

This overwrites the placeholder `lib/firebase_options.dart` with real values.
tvOS reads the `ios` entry automatically.

**B. Hand-fill:** copy `apiKey` / `appId` (GOOGLE_APP_ID) / `messagingSenderId`
(GCM_SENDER_ID) / `projectId` / `storageBucket` from your iOS app's
`GoogleService-Info.plist` (or Firebase console → Project settings) into the
`ios` block of `lib/firebase_options.dart`.

> **Optional — GoogleService-Info.plist:** the Dart options above are enough for
> Analytics. If you also want to drop the plist in, put your iOS app's
> `GoogleService-Info.plist` at `tvos/Runner/GoogleService-Info.plist` and add it
> to the Runner target in Xcode (drag it into the Runner group, tick
> "Copy items if needed" + the Runner target). Not required.

## 2. Run it

```bash
export PATH="/path/to/flutter-tvos/bin:$PATH"

# Simulator:
flutter-tvos pub get
open -a Simulator                         # boot a tvOS simulator
flutter-tvos run -d "Apple TV"            # or: flutter-tvos build tvos --simulator --debug

# Physical Apple TV (must be paired to Xcode: Xcode ▸ Devices & Simulators):
flutter-tvos run -d <your-apple-tv-name>
```

## 3. See events in Firebase DebugView (near-real-time)

Analytics normally batches events for ~1 hour. **DebugView** shows them within
seconds. Enable debug mode by passing a launch argument:

- **From Xcode:** open `tvos/Runner.xcworkspace` → scheme **Runner** ▸ Edit
  Scheme ▸ Run ▸ Arguments ▸ _Arguments Passed On Launch_ → add `-FIRDebugEnabled`.
  Run the Runner scheme.
- (To stop: use `-FIRDebugDisabled` once.)

Then in the app press **"logEvent: test_event"** (or any button) with the Siri
Remote. In the Firebase console open **Analytics ▸ DebugView** and select your
debug device — you'll see `test_event`, `screen_view`, `login`, etc. stream in
with their parameters within a few seconds.

> Simulator note: Analytics runs on the Simulator, but for a true end-to-end
> check use a **physical Apple TV in profile/AOT** (`flutter-tvos run --profile`)
> — that's what confirms the plugin under release-mode compilation.
