from pathlib import Path

def read_log_file(file_path):
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        lines = file.readlines()

    return [line.rstrip("\r\n") for line in lines]