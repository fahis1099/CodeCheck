
import ast


class CodeAnalyzer:
    """Analyzes the structure of Python source code."""

    def analyze(self, source_code):

        tree = ast.parse(source_code)

        results = {
            "imports": [],
            "functions": [],
            "classes": [],
            "loops": 0,
            "conditions": 0,
            "max_nesting": 0
        }

        for node in ast.walk(tree):

            # Detect imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    results["imports"].append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                results["imports"].append(node.module)

            # Detect functions
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                results["functions"].append(node.name)

            # Detect classes
            elif isinstance(node, ast.ClassDef):
                results["classes"].append(node.name)

            # Detect loops
            elif isinstance(node, (ast.For, ast.While)):
                results["loops"] += 1

            # Detect conditions
            elif isinstance(node, ast.If):
                results["conditions"] += 1

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
