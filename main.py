from pathlib import Path

from reader import read_log_file
from processor import process_log_lines
from reporter import generate_report, export_report_json


def main():
    project_dir = Path(__file__).parent

    input_file = project_dir / "data" / "system.log"
    output_file = project_dir / "output" / "report.json"

    try:
        lines = read_log_file(input_file)

        processed_data = process_log_lines(lines)

        report = generate_report(processed_data)

        export_report_json(report, output_file)

        print("Log analysis completed successfully.")
        print(f"Total lines: {report['summary']['total_lines']}")
        print(f"Valid entries: {report['summary']['valid_entries']}")
        print(f"Invalid entries: {report['summary']['invalid_entries']}")
        print(f"Report saved to: {output_file}")

    except OSError as error:
        print(f"File operation failed: {error}")


if __name__ == "__main__":
    main()