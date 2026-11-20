import json
from pathlib import Path

from processor import (
    count_severities,
    count_components,
    count_error_messages
)

def generate_report(processed_data):
    valid_records = processed_data["valid_records"]
    invalid_records = processed_data["invalid_records"]
    
    valid_entries = len(valid_records)
    invalid_entries = len(invalid_records)
    
    return {
        "summary": {
            "total_lines": valid_entries + invalid_entries,
            "valid_entries": valid_entries,
            "invalid_entries": invalid_entries
        },
        "severity_counts": count_severities(valid_records),
        "component_counts": count_components(valid_records),
        "error_message_counts": count_error_messages(valid_records)
    }
    
def export_report_json(report, file_path):
    path = Path(file_path)

    with path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)
    