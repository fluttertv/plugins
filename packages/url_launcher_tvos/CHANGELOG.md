## 0.0.2

* **Fix:** the privacy manifest now reaches the app when the package is linked
  through Swift Package Manager, which flutter-tvos uses for any plugin that
  ships a `tvos/Package.swift`. The SwiftPM target did not declare it, so the
  app was missing it, and App Store uploads could be rejected with ITMS-91061.
  `PrivacyInfo.xcprivacy` moves to `tvos/Classes/Resources/` (SwiftPM only
  bundles resources inside the target directory) and the podspec follows.

## 0.0.1

* Initial tvOS implementation of `url_launcher`, ported from `url_launcher_ios`
  6.4.1. External launches (`launchUrl`) and `canLaunchUrl` work via
  `UIApplication.open` / `canOpenURL`. The in-app browser modes
  (`inAppBrowserView` / `inAppWebView`) are unsupported on tvOS
  (no SafariServices): `supportsMode` reports `false`, and a launch requested
  with an in-app mode falls back to an external launch (the same fallback the
  browser-less macOS/Windows/Linux implementations make) rather than throwing.
  Unlike those three, `supportsMode` also reports `true` for
  `externalNonBrowserApplication`, since `universalLinksOnly` is forwarded to the host.
