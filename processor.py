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