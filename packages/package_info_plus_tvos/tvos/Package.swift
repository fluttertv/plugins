// swift-tools-version: 5.9
// Lets the package be consumed via Swift Package Manager. The target reuses
// the same `Classes/` sources the CocoaPods podspec compiles, so both
// dependency managers stay in sync from a single source tree.
import PackageDescription

let package = Package(
  name: "package_info_plus_tvos",
  platforms: [
    .tvOS(.v13),
  ],
  products: [
    .library(name: "package-info-plus-tvos", targets: ["package_info_plus_tvos"]),
  ],
  dependencies: [
    // Lets the target import Flutter. flutter-tvos generates a FlutterFramework
    // package (binary target wrapping Flutter.xcframework) as a sibling of this
    // package under the app's ephemeral SwiftPM packages, so `../FlutterFramework`
    // resolves at build time.
    .package(name: "FlutterFramework", path: "../FlutterFramework"),
  ],
  targets: [
    .target(
      name: "package_info_plus_tvos",
      dependencies: [
        .product(name: "FlutterFramework", package: "FlutterFramework"),
      ],
      path: "Classes",
      publicHeadersPath: "include/package_info_plus"
    ),
  ]
)
