
from analyzer.file_reader import FileReader
from analyzer.syntax_checker import SyntaxChecker

reader = FileReader()
checker = SyntaxChecker()

source = reader.read_file("sample_files/invalid.py")

result = checker.check_syntax(source)

print("\nSyntax Analysis Result:")
print(result)
