// swift-tools-version: 5.9
// Lets the package be consumed via Swift Package Manager. The target reuses
// the same `Classes/` sources the CocoaPods podspec compiles, so both
// dependency managers stay in sync from a single source tree.
import PackageDescription

// Keep in step with `version:` in pubspec.yaml and `s.version` in the podspec.
let libraryVersion = "0.0.2"

let package = Package(
  name: "cloud_firestore_tvos",
  platforms: [
    // Firebase 12.x requires tvOS 15.0, as in the podspec.
    .tvOS("15.0"),
  ],
  products: [
    .library(name: "cloud-firestore-tvos", targets: ["cloud_firestore_tvos"]),
  ],
  dependencies: [
    // The podspecs' `~> 12.15.0`. Every tvOS FlutterFire port declares this
    // same range, so an app resolves one firebase-ios-sdk for all of them.
    .package(url: "https://github.com/firebase/firebase-ios-sdk", .upToNextMinor(from: "12.15.0")),
    // FlutterFire's shared plugin registry. flutter-tvos places every SwiftPM
    // plugin side by side, so the sibling path resolves like FlutterFramework.
    // FirebaseCore comes in through it, from the same firebase-ios-sdk.
    .package(name: "firebase_core_tvos", path: "../firebase_core_tvos"),
    // Lets the target import Flutter. flutter-tvos generates a FlutterFramework
    // package as a sibling of this package under the app's ephemeral SwiftPM
    // packages, so `../FlutterFramework` resolves at build time.
    .package(name: "FlutterFramework", path: "../FlutterFramework"),
  ],
  targets: [
    // All Objective-C, so one target (SwiftPM cannot mix languages in one).
    .target(
      name: "cloud_firestore_tvos",
      dependencies: [
        // The podspec's Firebase/Firestore subspec.
        .product(name: "FirebaseFirestore", package: "firebase-ios-sdk"),
        .product(name: "firebase-core-tvos", package: "firebase_core_tvos"),
        .product(name: "FlutterFramework", package: "FlutterFramework"),
      ],
      path: "Classes",
      publicHeadersPath: "include/cloud_firestore/Public",
      cSettings: [
        .headerSearchPath("include/cloud_firestore/Private"),
        .headerSearchPath("include/cloud_firestore/Public"),
        // The podspec's GCC_PREPROCESSOR_DEFINITIONS.
        .define("LIBRARY_VERSION", to: "\"\(libraryVersion)\""),
        .define("LIBRARY_NAME", to: "\"flutter-fire-fst-tvos\""),
      ]
    ),
  ]
)
