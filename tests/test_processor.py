import pytest
from processor import (
    process_log_lines, 
    count_severities,
    count_components,
    filter_records,
    count_error_messages,
)

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
    
def test_count_severities():
    records = [
        {"severity": "INFO"},
        {"severity": "ERROR"},
        {"severity": "INFO"},
        {"severity": "CRITICAL"},
        {"severity": "WARNING"}
    ]
    
    result = count_severities(records)
    
    assert result == {
        "DEBUG": 0,
        "INFO": 2,
        "WARNING": 1,
        "ERROR": 1,
        "CRITICAL": 1
    }

def test_count_severities_empty_records():
    result = count_severities([])
    
    assert result == {
        "DEBUG": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0,
    }

def test_count_severities_single_level():
    records  = [
        {"severity": "ERROR"},
        {"severity": "ERROR"},
        {"severity": "ERROR"}
    ]
    
    result = count_severities(records)
    
    assert result == {
        "DEBUG": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 3,
        "CRITICAL": 0,
    }
    
def test_count_components():
    records = [
        {"component": "sensor"},
        {"component": "mqtt"},
        {"component": "sensor"},
        {"component": "system"},
        {"component": "mqtt"},
        {"component": "sensor"},
    ]
    
    result = count_components(records)
    
    assert result == {
        "sensor": 3,
        "mqtt": 2,
        "system": 1,
    }
    
def test_count_components_empty_records():
    result = count_components([])
    
    assert result == {}
    
def test_count_components_single_components():
     records = [
        {"component": "sensor"},
        {"component": "sensor"},
        {"component": "sensor"},
    ]
     
     result = count_components(records)
     
     assert result == {"sensor": 3} 
     
def test_filter_records_by_severities():
    records = [
        {"severity": "INFO", "component": "sensor"},
        {"severity": "ERROR", "component": "mqtt"},
        {"severity": "WARNING", "component": "sensor"},
        {"severity": "ERROR", "component": "sensor"},
    ]
    
    result = filter_records(records, severity="ERROR")
    
    assert result == [
        {"severity": "ERROR", "component": "mqtt"},
        {"severity": "ERROR", "component": "sensor"},
    ]

def test_filter_records_by_component():
    records = [
        {"severity": "INFO", "component": "sensor"},
        {"severity": "ERROR", "component": "mqtt"},
        {"severity": "WARNING", "component": "sensor"},
        {"severity": "ERROR", "component": "sensor"},
    ]
    
    result = filter_records(records, component="sensor")
    
    assert result == [
        {"severity": "INFO", "component": "sensor"},
        {"severity": "WARNING", "component": "sensor"},
        {"severity": "ERROR", "component": "sensor"}
    ]
    
def test_filter_records_by_severity_and_component():
    records = [
        {"severity": "INFO", "component": "sensor"},
        {"severity": "ERROR", "component": "mqtt"},
        {"severity": "WARNING", "component": "sensor"},
        {"severity": "ERROR", "component": "sensor"}
    ]
    
    result = filter_records(
        records,
        severity="ERROR",
        component="sensor"
    )
    
    assert result == [
        {"severity": "ERROR", "component": "sensor"}
    ]

def test_filter_records_without_filters():
    records  = [
        {"severity": "INFO", "component": "sensor"},
        {"severity": "ERROR", "component": "mqtt"},
    ]
    
    result = filter_records(records)
    
    assert result == records
    
def test_filter_records_no_matches():
    records = [
        {"severity": "INFO", "component": "sensor"},
        {"severity": "ERROR", "component": "mqtt"}
    ]
    
    result = filter_records(records, severity="CRITICAL")
    
    assert result == []
    
def test_filter_records_empty_input():
    result = filter_records([], severity="ERROR")
    
    assert result == []
    
def test_count_error_messages():
    records = [
        {"severity": "ERROR", "message": "Connection failed"},
        {"severity": "ERROR", "message": "Connection failed"},
        {"severity": "CRITICAL", "message": "Voltage critically low"},
        {"severity": "INFO", "message": "System operational"},
        {"severity": "WARNING", "message": "Temperature above threshold"},
    ]
    
    result = count_error_messages(records)
    
    assert result == {
        "Connection failed": 2,
        "Voltage critically low": 1,
    }
    
def test_count_error_messages_multiple_errors():
    records = [
        {"severity": "ERROR", "message": "Sensor timeout"},
        {"severity": "CRITICAL", "message": "Sensor timeout"},
        {"severity": "ERROR", "message": "MQTT connection failed"},
        {"severity": "ERROR", "message": "Sensor timeout"},
    ]
    
    result = count_error_messages(records)
    
    assert result == {
        "Sensor timeout": 3,
        "MQTT connection failed": 1,
    }
    
def test_count_error_messages_no_errors():
    records = [
        {"severity": "INFO", "message": "System operational"},
        {"severity": "WARNING", "message": "Temperature high"},
    ]
    
    result = count_error_messages(records)
    
    assert result == {}
    
def test_count_error_message_empty_input():
    result = count_error_messages([])
    
    assert result == {}


     
     