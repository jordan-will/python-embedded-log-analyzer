import pytest
from reader import read_log_file

def test_read_multiple_lines(tmp_path):
    log_file = tmp_path / "system.log"
    log_file.write_text(
         "First log entry\nSecond log entry\nThird log entry\n",
         encoding="utf-8"
    )

    result = read_log_file(log_file)

    assert result == [
        "First log entry",
        "Second log entry",
        "Third log entry",
    ]
    
def test_read_empty_file(tmp_path):
    log_file = tmp_path / "empty.log"
    log_file.write_text("", encoding="utf-8")
    
    result = read_log_file(log_file)
    
    assert result == []

def test_preserve_blank_lines(tmp_path):
    log_file = tmp_path / "blank.log"
    log_file.write_text(
        "First entry\n\nThird entry\n",
        encoding="utf-8"
    )
    
    result = read_log_file(log_file)
    
    assert result == [
         "First entry",
        "",
        "Third entry",
    ]
    
def test_missing_file_raises_error(tmp_path):
    log_file = tmp_path / "missing.log"
    
    with pytest.raises(FileNotFoundError):
        read_log_file(log_file)