# Project: Network Device Audit Tool

## Description
This project contains a Python script (`project.py`) that connects to network devices via SSH, audits their configuration for security settings, and generates a dated audit report. The script checks for:
- Telnet status
- HTTP server status
- Default SNMP community strings

## How It Works
- Uses Paramiko to connect to devices using SSH and a private key.
- Retrieves the running configuration from each device.
- Checks the configuration for insecure settings (Telnet, HTTP, SNMP).
- Generates a report file (e.g., `Audit_Report_2026-04-09.txt`) summarizing the findings for each device.

## How to Run
1. Ensure you have Python 3.x installed.
2. Install dependencies:
   ```bash
   pip install paramiko
   ```
3. Make sure your SSH private key is available at the path specified in the script.
4. Run the script:
   ```bash
   python project.py
   ```
5. The audit report will be saved in this folder.

## Requirements
- Python 3.x
- paramiko

## Network Environment
- The script is designed to connect to a virtual machine with the IP address `192.168.100.247`.
- Make sure this VM is running and accessible from your host machine.
- The VM should have SSH enabled and allow key-based authentication.

## Files
- `project.py`: Main audit script.
- `Audit_Report_YYYY-MM-DD.txt`: Example output report.

---
This project demonstrates automated network device auditing using Python and SSH.
