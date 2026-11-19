from datetime import datetime

VALID_SEVERITIES = {
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL"
}

def parse_log_line(line):
    fields = line.split("|")
    
    if len(fields) != 4:
        return {
            "valid": False,
            "record": None,
            "raw_line": line,
            "error": "Expected exactly 4 fields." 
        }
    
    timestamp, severity, component, message = [
        field.strip() for field in fields
    ]
    
    try:
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return {
            "valid": False,
            "record": None,
            "raw_line": line,
            "error": "Invalid timestamp."
        }
        
    if severity not in VALID_SEVERITIES:
        return {
            "valid": False,
            "record": None,
            "raw_line": line,
            "error": "Invalid severity."
        }
    
    if not component:
        return {
            "valid": False,
            "record": None,
            "raw_line": line,
            "error": "Component cannot be empty."
        }
    
    if not message:
        return {
            "valid": False,
            "record": None,
            "raw_line": line,
            "error": "Message cannot be empty."
        }
    
    return {
        "valid": True,
        "record": {
            "timestamp": timestamp,
            "severity": severity,
            "component": component,
            "message": message
        },
        "raw_line": line,
        "error": None
    }