
import json
from pathlib import Path


class ReportGenerator:
    """Generates text and JSON reports for code analysis."""

    def generate_report(self, file_path, syntax_result, analysis_result):

        report = {
            "file": Path(file_path).name,
            "syntax": syntax_result,
            "statistics": {
                "total_imports": len(analysis_result["imports"]),
                "unused_imports": analysis_result["unused_imports"],
                "total_functions": len(analysis_result["functions"]),
                "total_classes": len(analysis_result["classes"]),
                "total_loops": analysis_result["loops"],
                "total_conditions": analysis_result["conditions"],
                "maximum_nesting": analysis_result["max_nesting"]
            },
            "findings": []
        }

        # Add syntax findings
        if not syntax_result["valid"]:
            error = syntax_result["error"]

            report["findings"].append({
                "severity": "ERROR",
                "message": error["message"],
                "line": error["line"],
                "column": error["column"]
            })

        # Add unused import findings
        for name in analysis_result["unused_imports"]:
            report["findings"].append({
                "severity": "WARNING",
                "message": f"Unused import: {name}"
            })

        return report

    def generate_text_report(self, report):

        lines = [
            "=" * 45,
            "          CODECHECK ANALYSIS REPORT",
            "=" * 45,
            f"File: {report['file']}",
            "",
            "SYNTAX STATUS"
        ]

        if report["syntax"]["valid"]:
            lines.append("Status: VALID")
        else:
            lines.append("Status: INVALID")

        lines.extend([
            "",
            "CODE STATISTICS",
            "-" * 30
        ])

        for metric, value in report["statistics"].items():
            if metric == "unused_imports":
                value = ", ".join(value) if value else "None"

            lines.append(f"{metric}: {value}")

        lines.extend([
            "",
            "FINDINGS",
            "-" * 30
        ])

        if report["findings"]:
            for finding in report["findings"]:
                lines.append(
                    f"[{finding['severity']}] {finding['message']}"
                )

                if "line" in finding:
                    lines.append(
                        f"Line: {finding['line']}, "
                        f"Column: {finding['column']}"
                    )
        else:
            lines.append("No issues detected.")

        lines.append("=" * 45)

        return "\n".join(lines)

    def save_json_report(self, report, output_dir="reports"):

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        file_path = output_path / "analysis_report.json"

        with file_path.open("w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        return file_path

    def save_text_report(self, report, output_dir="reports"):

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        file_path = output_path / "analysis_report.txt"

        text = self.generate_text_report(report)

        file_path.write_text(text, encoding="utf-8")

        return file_path
