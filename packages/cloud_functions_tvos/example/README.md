# cloud_functions_tvos example (Apple TV)

Minimal app that invokes a Firebase **callable** Cloud Function from tvOS, to
verify the `cloud_functions_tvos` federated plugin on the Simulator and a
physical Apple TV.

## 1. Connect it to Firebase

On tvOS, `defaultTargetPlatform == TargetPlatform.iOS`, so the **iOS Firebase
app config is what tvOS uses** — no separate tvOS app needed.

```bash
cd packages/cloud_functions_tvos/example
flutterfire configure        # pick your project → select the iOS app
```
(or hand-fill `lib/firebase_options.dart`'s `ios` block from your iOS app's
`GoogleService-Info.plist` / the Firebase console).

Deploy a callable named `listFruit` (or edit the name in `lib/main.dart`):
```js
// functions/index.js
exports.listFruit = require("firebase-functions/v2/https")
  .onCall(() => ["apple", "banana", "cherry"]);
```

## 2. Run it

```bash
export PATH="/path/to/flutter-tvos/bin:$PATH"
flutter-tvos pub get
open -a Simulator                         # boot a tvOS simulator
flutter-tvos run -d "Apple TV"            # or a physical Apple TV
```

Press **call `httpsCallable("listFruit")`** with the Siri Remote. A returned
result (or even a `FirebaseFunctionsException` from the backend) confirms the
call reached Cloud Functions from Apple TV — i.e. the plugin works end-to-end.
