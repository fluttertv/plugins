// swift-tools-version: 5.9
// Lets the package be consumed via Swift Package Manager. The target reuses
// the same `Classes/` sources the CocoaPods podspec compiles, so both
// dependency managers stay in sync from a single source tree.
//
// flutter-tvos links a plugin that ships this file through SwiftPM and leaves
// it out of the Podfile. Every tvOS FlutterFire port that depends on this one
// ships a Package.swift too, and pulls this package in as
// `.package(path: "../firebase_core_tvos")`.
import PackageDescription

// Keep in step with `version:` in pubspec.yaml and `s.version` in the podspec.
let libraryVersion = "0.0.4"

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
    // The podspecs' `~> 12.15.0`. Every tvOS FlutterFire port declares this
    // same range, so an app resolves one firebase-ios-sdk for all of them.
    .package(url: "https://github.com/firebase/firebase-ios-sdk", .upToNextMinor(from: "12.15.0")),
    // Lets the target import Flutter. flutter-tvos generates a FlutterFramework
    // package as a sibling of this package under the app's ephemeral SwiftPM
    // packages, so `../FlutterFramework` resolves at build time.
    .package(name: "FlutterFramework", path: "../FlutterFramework"),
  ],
  targets: [
    // All Objective-C, so one target (SwiftPM cannot mix languages in one).
    // The headers under include/ are the module's public surface, which the
    // other tvOS FlutterFire ports import.
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
        .define("LIBRARY_VERSION", to: "\"\(libraryVersion)\""),
        .define("LIBRARY_NAME", to: "\"flutter-fire-core-tvos\""),
      ]
    ),
  ]
)
