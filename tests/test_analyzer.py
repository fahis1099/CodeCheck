
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

    unused_names = [
        item["name"] for item in result["unused_imports"]
    ]

    assert "os" in unused_names
    assert "math" not in unused_names


def test_aliased_import_detection():
    source = """
import math as m

def calculate(value):
    return m.sqrt(value)
"""
    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    assert result["unused_imports"] == []


def test_module_attribute_import_is_used():
    source = """
import math

def calculate():
    return math.sqrt(25)
"""
    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    unused_names = [
        item["name"] for item in result["unused_imports"]
    ]

    assert "math" not in unused_names


def test_import_used_inside_function():
    source = """
import os

def get_path():
    return os.getcwd()
"""
    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    unused_names = [
        item["name"] for item in result["unused_imports"]
    ]

    assert "os" not in unused_names


def test_multiple_imports():
    source = """
import os, math, json

def calculate():
    return math.sqrt(25)
"""
    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    unused_names = [
        item["name"] for item in result["unused_imports"]
    ]

    assert "math" not in unused_names
    assert "os" in unused_names
    assert "json" in unused_names


def test_from_import_used():
    source = """
from math import sqrt

def calculate():
    return sqrt(25)
"""
    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    assert result["unused_imports"] == []


def test_from_import_unused():
    source = """
from math import sqrt, pow

def calculate():
    return sqrt(25)
"""
    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    unused_names = [
        item["name"] for item in result["unused_imports"]
    ]

    assert "pow" in unused_names
    assert "sqrt" not in unused_names


def test_star_import_is_not_reported_as_unused():
    source = """
from math import *

def calculate():
    return sqrt(25)
"""
    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    assert result["unused_imports"] == []


def test_import_statistics_preserve_multiple_imports():
    source = """
import os, math, json

def calculate():
    return math.sqrt(25)
"""
    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    unused_names = [
        item["name"] for item in result["unused_imports"]
    ]

    assert len(result["imports"]) == 3
    assert "math" not in unused_names
    assert "os" in unused_names
    assert "json" in unused_names


def test_unused_import_line_number():
    source = """import os

def calculate():
    return 10
"""
    analyzer = CodeAnalyzer()
    result = analyzer.analyze(source)

    unused_import = next(
        item for item in result["unused_imports"]
        if item["name"] == "os"
    )

    assert unused_import["line"] == 1
