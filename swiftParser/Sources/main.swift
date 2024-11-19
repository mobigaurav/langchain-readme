// The Swift Programming Language
// https://docs.swift.org/swift-book

import SwiftSyntax

func parseSwiftFile(filePath: String) -> [String: Any] {
    var result: [String: Any] = [
        "classes": [String](),
        "functions": [String]()
    ]
    
    do {
        let sourceFile = try SyntaxParser.parse(URL(fileURLWithPath: filePath))
        
        sourceFile.walk(SyntaxVisitor { node in
            // Capture classes
            if let classDecl = node.as(ClassDeclSyntax.self) {
                result["classes"] = (result["classes"] as! [String]) + [classDecl.identifier.text]
            }
            // Capture functions
            if let funcDecl = node.as(FunctionDeclSyntax.self) {
                result["functions"] = (result["functions"] as! [String]) + [funcDecl.identifier.text]
            }
        })
        
    } catch {
        print("Failed to parse Swift file: \(error)")
    }
    return result
}

struct SyntaxVisitor: SyntaxVisitorProtocol {
    let visit: (Syntax) -> Void
    
    init(_ visit: @escaping (Syntax) -> Void) {
        self.visit = visit
    }
    
    func visitAny(_ node: Syntax) {
        visit(node)
    }
}

// Example: Read file path from command line arguments
if CommandLine.arguments.count < 2 {
    print("Usage: SwiftParser <file-path>")
    exit(1)
}

let filePath = CommandLine.arguments[1]
let parsedData = parseSwiftFile(filePath: filePath)

// Serialize to JSON for Python consumption
import Foundation
if let jsonData = try? JSONSerialization.data(withJSONObject: parsedData, options: .prettyPrinted),
   let jsonString = String(data: jsonData, encoding: .utf8) {
    print(jsonString)
}

