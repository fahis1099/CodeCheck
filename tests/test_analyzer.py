
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


def test_unused_import_detection():
    source = """
import os
import math

def calculate(a, b):
    return math.sqrt(a + b)
"""
    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    assert "os" in result["unused_imports"]
    assert "math" not in result["unused_imports"]


def test_aliased_import_detection():
    source = """
import math as m

def calculate(value):
    return m.sqrt(value)
"""
    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    assert result["unused_imports"] == []
