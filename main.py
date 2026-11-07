
import argparse

from analyzer.file_reader import FileReader
from analyzer.syntax_checker import SyntaxChecker
from analyzer.code_analyzer import CodeAnalyzer
from analyzer.report_generator import ReportGenerator


def main():
    parser = argparse.ArgumentParser(
        description="CodeCheck - Automated Python Code Analysis Tool"
    )

    parser.add_argument(
        "file",
        nargs="?",
        default="sample_files/example.py",
        help="Path to the Python file to analyze"
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        default="reports",
        help="Directory where analysis reports will be saved"
    )

    args = parser.parse_args()

    reader = FileReader()
    checker = SyntaxChecker()
    analyzer = CodeAnalyzer()
    reporter = ReportGenerator()

    try:
        source = reader.read_file(args.file)

        syntax_result = checker.check_syntax(source)

        if syntax_result["valid"]:
            analysis_result = analyzer.analyze(source)
        else:
            analysis_result = {
                "imports": [],
                "unused_imports": [],
                "mutable_defaults": [],
                "functions": [],
                "classes": [],
                "loops": 0,
                "conditions": 0,
                "max_nesting": 0
            }

        report = reporter.generate_report(
            args.file,
            syntax_result,
            analysis_result
        )

        print(reporter.generate_text_report(report))

        json_path = reporter.save_json_report(
            report, args.output_dir
        )

        text_path = reporter.save_text_report(
            report, args.output_dir
        )

        print("\nReports generated successfully!")
        print(f"JSON Report: {json_path}")
        print(f"Text Report: {text_path}")

        return 0 if syntax_result["valid"] else 1

    except (FileNotFoundError, ValueError, UnicodeDecodeError) as error:
        print(f"Error: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
