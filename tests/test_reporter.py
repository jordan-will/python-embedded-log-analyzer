import json

from reporter import generate_report, export_report_json

def test_generate_report_with_valid_invalid_records():
    processed_data = {
         "valid_records": [
            {
                "severity": "INFO",
                "component": "sensor",
                "message": "Reading received",
            },
            {
                "severity": "ERROR",
                "component": "mqtt",
                "message": "Connection failed",
            },
            {
                "severity": "ERROR",
                "component": "mqtt",
                "message": "Connection failed",
            },
            {
                "severity": "CRITICAL",
                "component": "power",
                "message": "Voltage critically low",
            },
        ],
        "invalid_records": [
            {
                "raw_line": "INVALID",
                "error": "Expected exactly 4 fields.",
            },
            {
                "raw_line": "BAD TIMESTAMP",
                "error": "Invalid timestamp.",
            },
        ],
    }
    
    report = generate_report(processed_data)
    
    assert report == {
        "summary": {
            "total_lines": 6,
            "valid_entries": 4,
            "invalid_entries": 2,
        },
        "severity_counts": {
            "DEBUG": 0,
            "INFO": 1,
            "WARNING": 0,
            "ERROR": 2,
            "CRITICAL": 1,
        },
        "component_counts": {
            "sensor": 1,
            "mqtt": 2,
            "power": 1,
        },
        "error_message_counts": {
            "Connection failed": 2,
            "Voltage critically low": 1,
        },
    }

def test_generate_report_with_empty_data():
    processed_data = {
        "valid_records": [],
        "invalid_records": [],
    }
    
    report = generate_report(processed_data)
    
    assert report == {
        "summary": {
            "total_lines": 0,
            "valid_entries": 0,
            "invalid_entries": 0,
        },
        "severity_counts": {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0,
        },
        "component_counts": {},
        "error_message_counts": {},
    }
    
def test_generate_report_with_only_valid_records():
    processed_data = {
        "valid_records": [
            {
                "severity": "WARNING",
                "component": "sensor",
                "message": "Temperature high",
            },
        ],
        "invalid_records": [],
    }

    report = generate_report(processed_data)

    assert report["summary"] == {
        "total_lines": 1,
        "valid_entries": 1,
        "invalid_entries": 0,
    }

    assert report["severity_counts"]["WARNING"] == 1
    assert report["component_counts"] == {"sensor": 1}
    assert report["error_message_counts"] == {}

def test_generate_report_with_only_invalid_records():
    processed_data = {
        "valid_records": [],
        "invalid_records": [
            {
                "raw_line": "INVALID 1",
                "error": "Malformed entry",
            },
            {
                "raw_line": "INVALID 2",
                "error": "Invalid timestamp",
            },
        ],
    }

    report = generate_report(processed_data)

    assert report["summary"] == {
        "total_lines": 2,
        "valid_entries": 0,
        "invalid_entries": 2,
    }

    assert report["severity_counts"] == {
        "DEBUG": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0,
    }

    assert report["component_counts"] == {}
    assert report["error_message_counts"] == {}
    
def test_export_report_json_creates_file(tmp_path):
    report = {
        "summary": {
            "total_lines": 2,
            "valid_entries": 1,
            "invalid_entries": 1,
        },
        "severity_counts": {
            "INFO": 1,
        },
    }

    output_file = tmp_path / "report.json"

    export_report_json(report, output_file)

    assert output_file.exists()

def test_export_report_json_preserves_data(tmp_path):
    report = {
        "summary": {
            "total_lines": 2,
            "valid_entries": 1,
            "invalid_entries": 1,
        },
        "severity_counts": {
            "INFO": 1,
            "ERROR": 0,
        },
        "component_counts": {
            "sensor": 1,
        },
        "error_message_counts": {},
    }

    output_file = tmp_path / "report.json"

    export_report_json(report, output_file)

    with output_file.open("r", encoding="utf-8") as file:
        exported_data = json.load(file)

    assert exported_data == report

def test_export_report_json_overwrites_existing_file(tmp_path):
    output_file = tmp_path / "report.json"
    output_file.write_text('{"old": "data"}', encoding="utf-8")

    report = {
        "summary": {
            "total_lines": 0,
            "valid_entries": 0,
            "invalid_entries": 0,
        },
    }

    export_report_json(report, output_file)

    with output_file.open("r", encoding="utf-8") as file:
        exported_data = json.load(file)

    assert exported_data == report