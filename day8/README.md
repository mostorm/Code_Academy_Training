
# Day 8: Network Scanning & Automation

## Description
- `nmap_scanner.py`: Scans a network for live hosts, saves results in JSON/YAML/XML.
- `converter.py`: Loads and displays scan results from different formats.
- `task2.py`: Automated configuration backup for network devices (Netmiko).
- `task2.md`: Task description and sample outputs.

## How They Work
- **nmap_scanner.py**: Uses the `nmap` library to scan a network and saves results in multiple formats.
- **converter.py**: Loads and prints scan results from JSON, YAML, and XML files.
- **task2.py**: Connects to network devices using Netmiko, retrieves running configs, and saves backups.

## How to Run
1. Install dependencies:
   ```bash
   pip install python-nmap pyyaml xmltodict netmiko
   ```
2. Run the scripts as needed:
   ```bash
   python nmap_scanner.py
   python converter.py
   python task2.py
   ```

## Requirements
- Python 3.x
- python-nmap
- pyyaml
- xmltodict
- netmiko
