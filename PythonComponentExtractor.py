import ast

class PythonComponentExtractor:
    def __init__(self, file_content):
        """
        Initializes the PythonComponentExtractor with the file content.

        Parameters:
        - file_content: The Python file content as a string.
        """
        self.file_content = file_content

    def extract_components(self):
        """
        Extracts classes, functions, and their docstrings from the Python code.

        Returns:
        - A dictionary with 'classes' and 'functions'.
        """
        components = {'classes': [], 'functions': []}
        try:
            tree = ast.parse(self.file_content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    components['classes'].append({
                        'name': node.name,
                        'docstring': ast.get_docstring(node)
                    })
                elif isinstance(node, ast.FunctionDef):
                    components['functions'].append({
                        'name': node.name,
                        'docstring': ast.get_docstring(node)
                    })
        except SyntaxError as e:
            print(f"Syntax error in file: {e}")
        return components
