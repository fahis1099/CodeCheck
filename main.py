
from analyzer.code_analyzer import CodeAnalyzer


def test_function_detection():

    source = """
def add(a, b):
    return a + b
"""

    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    assert "add" in result["functions"]


def test_class_detection():

    source = """
class Student:
    pass
"""

    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    assert "Student" in result["classes"]


def test_condition_detection():

    source = """
if True:
    print("Hello")
"""

    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    assert result["conditions"] == 1


def test_loop_detection():

    source = """
for i in range(5):
    print(i)
"""

    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    assert result["loops"] == 1


def test_nested_conditions():

    source = """
if True:
    if True:
        print("Nested")
"""

    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    assert result["max_nesting"] == 2
