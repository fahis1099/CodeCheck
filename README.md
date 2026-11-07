# CodeCheck

CodeCheck is a lightweight Python static code analysis tool. It reads Python source files, checks syntax, analyzes code structure, identifies selected code quality issues, and generates text and JSON reports.

The project is built with Python's Abstract Syntax Tree (AST) module. It analyzes source code without executing it.

## Features

- **File validation:** Reads Python files and checks file paths and encoding.
- **Syntax checking:** Detects Python syntax errors and reports their line and column.
- **Import analysis:** Lists imports and identifies potentially unused imports.
- **Code structure analysis:** Counts functions, classes, loops, and conditional statements.
- **Nesting analysis:** Calculates the maximum nesting depth of control structures.
- **Mutable default detection:** Flags list, dictionary, and set defaults in function definitions, including calls such as `list()`, `dict()`, and `set()`.
- **Exception handling check:** Detects bare `except:` clauses.
- **None comparison check:** Flags comparisons using `== None` or `!= None`; use `is None` or `is not None` instead.
- **Report generation:** Creates readable TXT and structured JSON reports.

## Technologies

- Python
- Abstract Syntax Tree (`ast`)
- argparse
- pytest

## Project structure

```text
CodeCheck/
├── analyzer/
│   ├── __init__.py
│   ├── file_reader.py
│   ├── syntax_checker.py
│   ├── code_analyzer.py
│   └── report_generator.py
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_cli.py
│   └── test_report_generator.py
├── sample_files/
│   ├── example.py
│   └── invalid_example.py
├── main.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/fahis1099/CodeCheck.git
cd CodeCheck
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Analyze the default sample file:

```bash
python main.py
```

Analyze a specific Python file:

```bash
python main.py path/to/your_file.py
```

Choose a report output directory:

```bash
python main.py path/to/your_file.py --output-dir my_reports
```

After analysis, CodeCheck prints a text summary and saves two files in the selected output directory:

- `analysis_report.txt`
- `analysis_report.json`

If no output directory is specified, reports are saved in `reports/`.

### Command-line exit codes

| Exit code | Meaning |
|---|---|
| `0` | File has valid Python syntax |
| `1` | Python syntax error detected |
| `2` | File or input error, such as a missing file or unsupported encoding |

## Example checks

CodeCheck reports these patterns:

```python
import os  # Potentially unused import

def add_item(item, items=[]):  # Mutable default argument
    try:
        return items + [item]
    except:  # Bare except clause
        return None

if item == None:  # Prefer: item is None
    print("No item")
```

The import usage and selected code quality checks are heuristic AST-based checks. They are not a complete replacement for a production-grade linter or type checker.

## Running tests

Run the complete test suite from the project root:

```bash
python -m pytest -v
```

The current test suite contains **40 tests** covering the analyzer, command-line behavior, and report generation.

## Current scope

CodeCheck is a learning-focused static analysis project. It currently checks selected syntax and code quality patterns. It does not execute analyzed files, modify source code, or provide a complete security audit.

## Author

**Mohammed Fahis M**

- GitHub: [fahis1099](https://github.com/fahis1099)
