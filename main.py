
from analyzer.file_reader import FileReader
from analyzer.syntax_checker import SyntaxChecker
from analyzer.code_analyzer import CodeAnalyzer
from analyzer.report_generator import ReportGenerator


def main():

    file_path = "sample_files/example.py"

    reader = FileReader()
    checker = SyntaxChecker()
    analyzer = CodeAnalyzer()
    reporter = ReportGenerator()

    try:
        # Step 1: Read source file
        source = reader.read_file(file_path)

        # Step 2: Check syntax
        syntax_result = checker.check_syntax(source)

        # Step 3: Analyze only if syntax is valid
        if syntax_result["valid"]:
            analysis_result = analyzer.analyze(source)

        else:
            analysis_result = {
                "imports": [],
                "unused_imports": [],
                "functions": [],
                "classes": [],
                "loops": 0,
                "conditions": 0,
                "max_nesting": 0
            }

        # Step 4: Generate report
        report = reporter.generate_report(
            file_path,
            syntax_result,
            analysis_result
        )

        # Step 5: Display report
        print(reporter.generate_text_report(report))

        # Step 6: Save reports
        json_path = reporter.save_json_report(report)
        text_path = reporter.save_text_report(report)

        print("\nReports generated successfully!")
        print(f"JSON Report: {json_path}")
        print(f"Text Report: {text_path}")

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
