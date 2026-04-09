
# Day 3: Firewall Log Analysis

## Description
- `task.py`: Parses and analyzes firewall logs, generates CSV, JSON, and threat reports.

## How It Works
- Reads `firewall.log` line by line.
- Uses regular expressions to extract log fields (timestamp, action, protocol, IPs, ports, etc.).
- Validates IP addresses.
- Counts actions, top destination ports, and suspicious IPs (appearing 3+ times).
- Outputs:
  - `output.csv`: Parsed log entries in CSV format.
  - `output.json`: Parsed log entries in JSON format.
  - `threats.txt`: List of suspicious IPs.
- Prints a summary to the terminal.

## How to Run
1. Place your firewall log in `firewall.log`.
2. Open a terminal in this folder.
3. Run:
   ```bash
   python task.py
   ```

## Requirements
- Python 3.x
- No external libraries required (uses built-in `re`, `csv`, `json`, `collections`).
