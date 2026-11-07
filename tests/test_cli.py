
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "main.py", *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )


def test_cli_default_file():
    result = run_cli()

    assert result.returncode == 0
    assert "CODECHECK ANALYSIS REPORT" in result.stdout
    assert "Status: VALID" in result.stdout


def test_cli_custom_file():
    result = run_cli("sample_files/example.py")

    assert result.returncode == 0
    assert "File: example.py" in result.stdout


def test_cli_custom_output_directory(tmp_path):
    result = run_cli(
        "sample_files/example.py",
        "--output-dir",
        str(tmp_path)
    )

    assert result.returncode == 0
    assert (tmp_path / "analysis_report.json").exists()
    assert (tmp_path / "analysis_report.txt").exists()


def test_cli_missing_file():
    result = run_cli("sample_files/unknown.py")

    assert result.returncode == 2
    assert "File not found" in result.stdout


def test_cli_help():
    result = run_cli("--help")

    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "--output-dir" in result.stdout

def test_cli_invalid_syntax(tmp_path):
    invalid_file = tmp_path / "invalid.py"

    invalid_file.write_text(
        "def calculate(a, b)\n    return a + b",
        encoding="utf-8"
    )

    result = run_cli(
        str(invalid_file),
        "--output-dir",
        str(tmp_path / "reports")
    )

    assert result.returncode == 1
    assert "Status: INVALID" in result.stdout
    assert "expected ':'" in result.stdout

    assert (tmp_path / "reports" / "analysis_report.json").exists()
    assert (tmp_path / "reports" / "analysis_report.txt").exists()