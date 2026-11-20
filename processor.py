from parser import parse_log_line

def process_log_lines(lines):
    valid_records = []
    invalid_record = []
    
    for line in lines:
        result = parse_log_line(line)
        
        if result["valid"]:
            valid_records.append(result["record"])
        else:
            invalid_record.append({
                "raw_line": result["raw_line"],
                "error": result["error"]
            })
    
    return {
        "valid_records": valid_records,
        "invalid_records": invalid_record
    }
    
def count_severities(records):
    severities = [
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL"
    ]
    
    counts = {
        severity: 0
        for severity in severities
    }
    
    for record in records:
        counts[record["severity"]] += 1
    
    return counts

def count_components(records):
    counts = {}
    
    for record in records:
        component = record["component"]
        
        if component not in counts:
            counts[component] = 0
        
        counts[component] += 1
    
    return counts

def filter_records(records, severity=None, component=None):
    filtered_records = []
    
    for record in records:
        if severity is not None and record["severity"] != severity:
            continue
        if component is not None and record["component"] != component:
            continue
        
        filtered_records.append(record)
        
    return filtered_records

def count_error_messages(records):
    counts = {}

    for record in records:
        if record["severity"] not in ("ERROR", "CRITICAL"):
            continue

        message = record["message"]
        counts[message] = counts.get(message, 0) + 1

    return counts
    
        