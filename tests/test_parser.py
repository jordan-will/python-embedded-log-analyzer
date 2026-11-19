
import pytest

from parser import parse_log_line


def test_parse_valid_log_line():
    line = (
        "2026-11-19 09:15:30|INFO|sensor|"
        "Temperature reading received"
    )

    result = parse_log_line(line)

    assert result == {
        "valid": True,
        "record": {
            "timestamp": "2026-11-19 09:15:30",
            "severity": "INFO",
            "component": "sensor",
            "message": "Temperature reading received",
        },
        "raw_line": line,
        "error": None,
    }


@pytest.mark.parametrize(
    ("line", "expected_error"),
    [
        (
            "INVALID LOG ENTRY",
            "Expected exactly 4 fields.",
        ),
        (
            "2026-99-99 09:15:30|INFO|sensor|Invalid timestamp",
            "Invalid timestamp.",
        ),
        (
            "2026-11-19 09:15:30|UNKNOWN|sensor|Invalid severity",
            "Invalid severity.",
        ),
        (
            "2026-11-19 09:15:30|INFO||Missing component",
            "Component cannot be empty.",
        ),
        (
            "2026-11-19 09:15:30|INFO|sensor|",
            "Message cannot be empty.",
        ),
        (
            "",
            "Expected exactly 4 fields.",
        ),
    ],
)
def test_parse_invalid_log_lines(line, expected_error):
    result = parse_log_line(line)

    assert result["valid"] is False
    assert result["record"] is None
    assert result["raw_line"] == line
    assert result["error"] == expected_error
