import pytest
from processor import process_log_lines

@pytest.fixture
def sample_log_lines():
     return [
        "2026-11-19 09:15:30|INFO|sensor|Temperature reading received",
        "INVALID LOG ENTRY",
        "2026-11-19 09:15:32|ERROR|mqtt|Connection failed",
        "2026-99-99 09:15:33|INFO|system|Invalid timestamp",
    ]
     
def test_process_mixed_log_lines(sample_log_lines):
    result = process_log_lines(sample_log_lines)
    
    assert len(result["valid_records"]) == 2
    assert len(result["invalid_records"]) == 2
    
    assert result["valid_records"][0] == {
         "timestamp": "2026-11-19 09:15:30",
        "severity": "INFO",
        "component": "sensor",
        "message": "Temperature reading received",
    }
    
    assert result["invalid_records"][0] == {
        "raw_line": "INVALID LOG ENTRY",
        "error": "Expected exactly 4 fields.",
    }
    
def test_result_empty_list():
    result = process_log_lines([])
    
    assert result == {
        "valid_records": [],
        "invalid_records": []
    }
    
def test_process_onlly_valid_lines():
    lines = [
        "2026-11-19 09:15:30|INFO|sensor|Reading received",
        "2026-11-19 09:15:31|DEBUG|system|System check",
    ]
     
    result = process_log_lines(lines)
    
    assert len(result["valid_records"])  == 2
    assert result["invalid_records"] == []
    
     
     