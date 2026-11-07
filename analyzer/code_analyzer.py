
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


class MutableDefaultVisitor(ast.NodeVisitor):
    """Detects mutable default arguments in functions."""

    MUTABLE_TYPES = (ast.List, ast.Dict, ast.Set)

    MUTABLE_CALLS = {"list", "dict", "set"}

    def __init__(self):
        self.findings = []

    def visit_FunctionDef(self, node):
        self._check_defaults(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self._check_defaults(node)
        self.generic_visit(node)

    def _check_defaults(self, node):

        positional_args = node.args.posonlyargs + node.args.args
        defaults = node.args.defaults

        # Positional defaults align with the last positional arguments.
        default_args = positional_args[len(positional_args) - len(defaults):]

        for argument, default in zip(default_args, defaults):

            if self._is_mutable(default):
                self.findings.append({
                    "name": argument.arg,
                    "line": default.lineno
                })

        # Check keyword-only arguments with defaults.
        for argument, default in zip(
            node.args.kwonlyargs,
            node.args.kw_defaults
        ):

            if default is not None and self._is_mutable(default):
                self.findings.append({
                    "name": argument.arg,
                    "line": default.lineno
                })

    def _is_mutable(self, node):

        if isinstance(node, self.MUTABLE_TYPES):
            return True

        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in self.MUTABLE_CALLS
        ):
            return True

        return False


class CodeAnalyzer:
    """Analyzes the structure of Python source code."""

    def analyze(self, source_code):

        tree = ast.parse(source_code)

        results = {
            "imports": [],
            "unused_imports": [],
            "mutable_defaults": [],
            "functions": [],
            "classes": [],
            "loops": 0,
            "conditions": 0,
            "max_nesting": 0
        }

        visitor = ImportUsageVisitor()
        visitor.visit(tree)

        mutable_visitor = MutableDefaultVisitor()
        mutable_visitor.visit(tree)

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
        results["unused_imports"] = [
            {
                "name": item["local_name"],
                "line": item["line"]
            }
            for item in visitor.imports
            if not item["star_import"]
            and item["local_name"] not in visitor.used_names
        ]

        # Identify mutable default arguments.
        results["mutable_defaults"] = mutable_visitor.findings

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
