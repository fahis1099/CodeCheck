
import ast


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

        imported_names = set()
        used_names = set()

        for node in ast.walk(tree):

            # Detect regular imports
            if isinstance(node, ast.Import):

                for alias in node.names:

                    results["imports"].append(alias.name)

                    if alias.asname:
                        imported_names.add(alias.asname)
                    else:
                        imported_names.add(alias.name.split(".")[0])

            # Detect from-import statements
            elif isinstance(node, ast.ImportFrom):

                for alias in node.names:

                    if alias.name == "*":
                        continue

                    results["imports"].append(alias.name)

                    imported_names.add(
                        alias.asname if alias.asname else alias.name
                    )

            # Detect variable and name references
            elif isinstance(node, ast.Name):

                used_names.add(node.id)

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

        # Identify unused imports
        results["unused_imports"] = sorted(
            imported_names - used_names
        )

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
