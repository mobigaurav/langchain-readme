import javalang

class JavaParser:
    def parse(self, content):
        components = {"classes": [], "methods": []}
        tree = javalang.parse.parse(content)
        for _, node in tree.filter(javalang.tree.ClassDeclaration):
            components["classes"].append(node.name)
        for _, node in tree.filter(javalang.tree.MethodDeclaration):
            components["methods"].append(node.name)
        return components
