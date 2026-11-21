# Embedded System Log Analyzer

A modular Python application for reading, parsing, validating, analyzing, and reporting embedded system log files.

## Project Objective

A practical log analysis tool capable of processing structured log records, identifying malformed entries, generating statistics, filtering records, and exporting consolidated reports in JSON format.

The project applies Python fundamentals, modular programming, file handling, data processing, exception handling, JSON serialization, and automated testing.

## Features

- Read log files using UTF-8 encoding.
- Parse structured log records.
- Validate timestamps, severity levels, and required fields.
- Identify and separate malformed records.
- Count log entries by severity.
- Count log entries by component.
- Filter records by severity and component.
- Count recurring messages with `ERROR` and `CRITICAL` severity.
- Generate consolidated analysis reports.
- Export reports in JSON format.
- Handle file operation errors.

## Log Format

Each log entry must follow this structure:

```text
timestamp|severity|component|message
```

Example:

```text
2026-11-20 10:30:00|INFO|Sensor|Temperature reading received
2026-11-20 10:31:00|WARNING|Network|Connection latency detected
2026-11-20 10:32:00|ERROR|Storage|Failed to write data
```

Supported severity levels:

- `DEBUG`
- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`

Malformed records are identified and included in the report as invalid entries.

## Technologies

- Python 3.12
- pytest
- Git
- JSON
- Python standard library

## Project Structure

```text
p1-embedded-log-analyzer/
├── data/
│   └── system.log
├── output/
│   ├── .gitkeep
│   └── report.json
├── tests/
│   ├── test_reader.py
│   ├── test_parser.py
│   ├── test_processor.py
│   └── test_reporter.py
├── main.py
├── reader.py
├── parser.py
├── processor.py
├── reporter.py
├── pytest.ini
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Clone the repository and navigate to the project directory.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the development dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Place the input log file at:

```text
data/system.log
```

Run the application:

```bash
python main.py
```

The application processes the input file and generates the report at:

```text
output/report.json
```

The terminal displays a summary containing the total number of lines, valid entries, invalid entries, and report location.

## Running Tests

Run the complete automated test suite:

```bash
pytest -v
```

Run tests for a specific module:

```bash
pytest tests/test_reader.py -v
pytest tests/test_parser.py -v
pytest tests/test_processor.py -v
pytest tests/test_reporter.py -v
```

## Architecture

The application follows a modular structure with clearly separated responsibilities:

| Module | Responsibility |
|---|---|
| `main.py` | Coordinates the application workflow |
| `reader.py` | Reads log files |
| `parser.py` | Parses and validates individual log entries |
| `processor.py` | Processes records, filters entries, and calculates statistics |
| `reporter.py` | Generates reports and exports JSON files |

### Data Flow

```text
Input Log File
      |
      v
   reader.py
      |
      v
  processor.py
      |
      v
   parser.py
      |
      v
Processed Records
      |
      v
  reporter.py
      |
      v
  JSON Report
```

`processor.py` calls `parser.py` to validate individual records. The reporter reuses processing functions to calculate statistics.

## Author
Jordan Willian Marques Pereira
E-mail: jordan.willian.mp@gmail.com