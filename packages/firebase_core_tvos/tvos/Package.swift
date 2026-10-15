// swift-tools-version: 5.9
// Lets the package be consumed via Swift Package Manager. The target reuses
// the same `Classes/` sources the CocoaPods podspec compiles, so both
// dependency managers stay in sync from a single source tree.
import PackageDescription

let package = Package(
  name: "firebase_core_tvos",
  platforms: [
    // Firebase 12.x requires tvOS 15.0, as in the podspec.
    .tvOS("15.0"),
  ],
  products: [
    .library(name: "firebase-core-tvos", targets: ["firebase_core_tvos"]),
  ],
  dependencies: [
    // Any Firebase 12.x from the podspec's 12.15.0: every Firebase plugin in an
    // app must agree on one firebase-ios-sdk, and the tvOS ports ship separately.
    .package(url: "https://github.com/firebase/firebase-ios-sdk", from: "12.15.0"),
    // Lets the target import Flutter. flutter-tvos generates a FlutterFramework
    // package (binary target wrapping Flutter.xcframework) as a sibling of this
    // package under the app's ephemeral SwiftPM packages, so `../FlutterFramework`
    // resolves at build time.
    .package(name: "FlutterFramework", path: "../FlutterFramework"),
  ],
  targets: [
    // All Objective-C, so one target (SwiftPM cannot mix languages in one).
    // The headers under include/ are the module's public surface, which
    // firebase_analytics_tvos and the other tvOS FlutterFire ports import.
    .target(
      name: "firebase_core_tvos",
      dependencies: [
        .product(name: "FirebaseCore", package: "firebase-ios-sdk"),
        .product(name: "FirebaseInstallations", package: "firebase-ios-sdk"),
        .product(name: "FlutterFramework", package: "FlutterFramework"),
      ],
      path: "Classes",
      publicHeadersPath: "include",
      cSettings: [
        .headerSearchPath("include/firebase_core"),
        .headerSearchPath("include"),
        // The podspec's GCC_PREPROCESSOR_DEFINITIONS.
        .define("LIBRARY_VERSION", to: "\"0.0.1\""),
        .define("LIBRARY_NAME", to: "\"flutter-fire-core-tvos\""),
      ]
    ),
  ]
)
