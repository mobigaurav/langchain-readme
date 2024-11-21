// swift-tools-version: 6.0
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "swiftParser",
    platforms: [
        .macOS(.v12)
    ],
    dependencies: [
        // Add SwiftSyntax as a dependency
        .package(url: "https://github.com/apple/swift-syntax.git", from: "0.50700.0")
    ],
    targets: [
        // Define the executable target
        .executableTarget(
            name: "swiftParser",
            dependencies: [
                .product(name: "SwiftSyntax", package: "swift-syntax")
            ],
            path: "Sources/swiftParser" // Ensure this path exists
        ),
        // Define the library target
        .target(
            name: "SwiftParser",
            dependencies: [
                .product(name: "SwiftSyntax", package: "swift-syntax")
            ],
            path: "Sources/SwiftParser" // Ensure this path exists
        )
    ]
)
