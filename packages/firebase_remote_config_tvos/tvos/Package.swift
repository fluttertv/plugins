// swift-tools-version: 5.9
// Lets the package be consumed via Swift Package Manager. The target reuses
// the same `Classes/` sources the CocoaPods podspec compiles, so both
// dependency managers stay in sync from a single source tree.
import PackageDescription

let package = Package(
  name: "firebase_remote_config_tvos",
  platforms: [
    // Firebase 12.x requires tvOS 15.0, as in the podspec.
    .tvOS("15.0"),
  ],
  products: [
    .library(name: "firebase-remote-config-tvos", targets: ["firebase_remote_config_tvos"]),
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
    .target(
      name: "firebase_remote_config_tvos",
      dependencies: [
        // The podspec's Firebase/RemoteConfig subspec.
        .product(name: "FirebaseRemoteConfig", package: "firebase-ios-sdk"),
        .product(name: "firebase-core-tvos", package: "firebase_core_tvos"),
        .product(name: "FlutterFramework", package: "FlutterFramework"),
      ],
      path: "Classes",
      swiftSettings: [
        // Keep Swift `#if TARGET_OS_TV` branches active, matching the podspec.
        .define("TARGET_OS_TV"),
      ]
    ),
  ]
)
