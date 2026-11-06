
import ast


class SyntaxChecker:
    """Checks Python source code for syntax errors."""

    def check_syntax(self, source_code):

        try:
            ast.parse(source_code)

            return {
                "valid": True,
                "error": None
            }

        except SyntaxError as error:

            return {
                "valid": False,
                "error": {
                    "message": error.msg,
                    "line": error.lineno,
                    "column": error.offset
                }
            }

