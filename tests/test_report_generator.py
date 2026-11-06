
from analyzer.report_generator import ReportGenerator


def test_report_generation():

    syntax_result = {
        "valid": True,
        "error": None
    }

    analysis_result = {
        "imports": ["os", "math"],
        "unused_imports": ["os"],
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
