
from analyzer.report_generator import ReportGenerator


def test_report_generation():

    syntax_result = {
        "valid": True,
        "error": None
    }

    analysis_result = {
        "imports": ["os", "math"],
        "unused_imports": [{"name": "os", "line": 1}],
        "mutable_defaults": [],
        "bare_except": [],
        "none_comparisons": [],
        "functions": ["calculate"],
        "classes": ["Student"],
        "loops": 1,
        "conditions": 2,
        "max_nesting": 2
    }

    generator = ReportGenerator()

    report = generator.generate_report(
        "example.py",
        syntax_result,
        analysis_result
    )

    assert report["file"] == "example.py"
    assert report["statistics"]["total_imports"] == 2
    assert report["statistics"]["total_functions"] == 1
    assert len(report["findings"]) == 1


def test_json_report_saving(tmp_path):

    generator = ReportGenerator()

    report = {
        "file": "example.py",
        "syntax": {"valid": True, "error": None},
        "statistics": {},
        "findings": []
    }

    file_path = generator.save_json_report(
        report,
        output_dir=tmp_path
    )

    assert file_path.exists()
    assert file_path.suffix == ".json"


def test_text_report_saving(tmp_path):

    generator = ReportGenerator()

    report = {
        "file": "example.py",
        "syntax": {"valid": True, "error": None},
        "statistics": {},
        "findings": []
    }

    file_path = generator.save_text_report(
        report,
        output_dir=tmp_path
    )

    assert file_path.exists()
    assert file_path.suffix == ".txt"


def test_unused_import_line_in_report():

    generator = ReportGenerator()

    syntax_result = {
        "valid": True,
        "error": None
    }

    analysis_result = {
        "imports": ["os"],
        "unused_imports": [
            {"name": "os", "line": 1}
        ],
        "mutable_defaults": [],
        "bare_except": [],
        "none_comparisons": [],
        "functions": [],
        "classes": [],
        "loops": 0,
        "conditions": 0,
        "max_nesting": 0
    }

    report = generator.generate_report(
        "example.py",
        syntax_result,
        analysis_result
    )

    assert report["findings"][0]["line"] == 1

    text = generator.generate_text_report(report)

    assert "Unused import: os" in text
    assert "Line: 1" in text


def test_mutable_default_finding_in_report():

    generator = ReportGenerator()

    syntax_result = {
        "valid": True,
        "error": None
    }

    analysis_result = {
        "imports": [],
        "unused_imports": [],
        "mutable_defaults": [
            {"name": "items", "line": 3}
        ],
        "bare_except": [],
        "none_comparisons": [],
        "functions": ["add_item"],
        "classes": [],
        "loops": 0,
        "conditions": 0,
        "max_nesting": 0
    }

    report = generator.generate_report(
        "example.py",
        syntax_result,
        analysis_result
    )

    finding = report["findings"][0]

    assert finding["severity"] == "WARNING"
    assert finding["message"] == "Mutable default argument: items"
    assert finding["line"] == 3
    assert report["statistics"]["mutable_defaults"] == 1

    text = generator.generate_text_report(report)

    assert "Mutable default argument: items" in text
    assert "Line: 3" in text


def test_bare_except_finding_in_report():

    generator = ReportGenerator()

    syntax_result = {
        "valid": True,
        "error": None
    }

    analysis_result = {
        "imports": [],
        "unused_imports": [],
        "mutable_defaults": [],
        "bare_except": [
            {"line": 4}
        ],
        "none_comparisons": [],
        "functions": [],
        "classes": [],
        "loops": 0,
        "conditions": 0,
        "max_nesting": 0
    }

    report = generator.generate_report(
        "example.py",
        syntax_result,
        analysis_result
    )

    finding = report["findings"][0]

    assert finding["severity"] == "WARNING"
    assert finding["message"] == "Bare except clause detected"
    assert finding["line"] == 4
    assert report["statistics"]["bare_except"] == 1

    text = generator.generate_text_report(report)

    assert "Bare except clause detected" in text
    assert "Line: 4" in text


def test_none_comparison_finding_in_report():

    generator = ReportGenerator()

    syntax_result = {
        "valid": True,
        "error": None
    }

    analysis_result = {
        "imports": [],
        "unused_imports": [],
        "mutable_defaults": [],
        "bare_except": [],
        "none_comparisons": [
            {"line": 5}
        ],
        "functions": [],
        "classes": [],
        "loops": 0,
        "conditions": 1,
        "max_nesting": 0
    }

    report = generator.generate_report(
        "example.py",
        syntax_result,
        analysis_result
    )

    finding = report["findings"][0]

    assert finding["severity"] == "WARNING"
    assert "is None" in finding["message"]
    assert finding["line"] == 5
    assert report["statistics"]["none_comparisons"] == 1

    text = generator.generate_text_report(report)

    assert "Use 'is None' or 'is not None'" in text
    assert "Line: 5" in text
