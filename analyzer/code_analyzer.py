
import ast


class ImportUsageVisitor(ast.NodeVisitor):
    """Collects import declarations and referenced names."""

    def __init__(self):
        self.imports = []
        self.used_names = set()

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name.split(".")[0]

            self.imports.append({
                "name": alias.name,
                "local_name": name,
                "line": node.lineno,
                "star_import": False
            })

    def visit_ImportFrom(self, node):
        for alias in node.names:
            is_star = alias.name == "*"

            self.imports.append({
                "name": alias.name,
                "local_name": alias.asname or alias.name,
                "line": node.lineno,
                "star_import": is_star
            })

    def visit_Name(self, node):
        self.used_names.add(node.id)


class CodeAnalyzer:
    """Analyzes the structure of Python source code."""

    def analyze(self, source_code):

        tree = ast.parse(source_code)

        results = {
            "imports": [],
            "unused_imports": [],
            "functions": [],
            "classes": [],
            "loops": 0,
            "conditions": 0,
            "max_nesting": 0
        }

        visitor = ImportUsageVisitor()
        visitor.visit(tree)

        for node in ast.walk(tree):

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                results["functions"].append(node.name)

            elif isinstance(node, ast.ClassDef):
                results["classes"].append(node.name)

            elif isinstance(node, (ast.For, ast.While)):
                results["loops"] += 1

            elif isinstance(node, ast.If):
                results["conditions"] += 1

        # Preserve the existing imports output format.
        results["imports"] = [
            item["name"] for item in visitor.imports
        ]

        # Identify potentially unused imports.
        results["unused_imports"] = sorted({
            item["local_name"]
            for item in visitor.imports
            if not item["star_import"]
            and item["local_name"] not in visitor.used_names
        })

        results["max_nesting"] = self._calculate_nesting(tree)

        return results

    def _calculate_nesting(self, node, depth=0):

        max_depth = depth

        for child in ast.iter_child_nodes(node):

            if isinstance(child, (ast.If, ast.For, ast.While)):
                child_depth = self._calculate_nesting(
                    child, depth + 1
                )
            else:
                child_depth = self._calculate_nesting(
                    child, depth
                )

            max_depth = max(max_depth, child_depth)

        return max_depth
