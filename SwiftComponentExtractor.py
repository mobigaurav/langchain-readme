import subprocess
import json

def parse_swift_file_with_swiftsyntax(file_path):
    """
    Parses a Swift file using SwiftSyntax and returns the parsed data.

    Parameters:
    - file_path: Path to the Swift file.

    Returns:
    - A dictionary containing classes and functions in the Swift file.
    """
    try:
        result = subprocess.run(
            ["./SwiftParser/.build/debug/SwiftParser", file_path],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return {}

# Example usage
swift_file = "example.swift"
parsed_data = parse_swift_file_with_swiftsyntax(swift_file)
print(parsed_data)
