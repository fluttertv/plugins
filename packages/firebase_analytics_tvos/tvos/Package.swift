// swift-tools-version: 5.9
// Lets the package be consumed via Swift Package Manager. The target reuses
// the same `Classes/` sources the CocoaPods podspec compiles, so both
// dependency managers stay in sync from a single source tree.
import PackageDescription

let package = Package(
  name: "firebase_analytics_tvos",
  platforms: [
    // Firebase 12.x requires tvOS 15.0, as in the podspec.
    .tvOS("15.0"),
  ],
  products: [
    .library(name: "firebase-analytics-tvos", targets: ["firebase_analytics_tvos"]),
  ],
  dependencies: [
    // Any Firebase 12.x from the podspec's 12.15.0: every Firebase plugin in an
    // app must agree on one firebase-ios-sdk, and the tvOS ports ship separately.
    .package(url: "https://github.com/firebase/firebase-ios-sdk", from: "12.15.0"),
    // A sibling under the app's ephemeral SwiftPM packages, like FlutterFramework.
    .package(name: "firebase_core_tvos", path: "../firebase_core_tvos"),
    // Lets the target import Flutter. flutter-tvos generates a FlutterFramework
    // package (binary target wrapping Flutter.xcframework) as a sibling of this
    // package under the app's ephemeral SwiftPM packages, so `../FlutterFramework`
    // resolves at build time.
    .package(name: "FlutterFramework", path: "../FlutterFramework"),
  ],
  targets: [
    .target(
      name: "firebase_analytics_tvos",
      dependencies: [
        .product(name: "FirebaseAnalytics", package: "firebase-ios-sdk"),
        .product(name: "firebase-core-tvos", package: "firebase_core_tvos"),
        .product(name: "FlutterFramework", package: "FlutterFramework"),
      ],
      path: "Classes"
    ),
  ]
)
