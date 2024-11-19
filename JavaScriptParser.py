import re

class JavaScriptParser:
    def parse(self, content):
        components = {
            "functions": re.findall(r'function\s+(\w+)', content),
            "classes": re.findall(r'class\s+(\w+)', content)
        }
        return components
