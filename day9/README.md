
# Day 9: Nmap Scan & Email Notification

## Description
- `task.py`: Performs a network scan and emails the results (using `yagmail`).

## How It Works
- Scans the network for live hosts using `nmap`.
- Saves results to a JSON file.
- Sends the results via email using `yagmail` and credentials from a `.env` file.

## How to Run
1. Install dependencies:
   ```bash
   pip install python-nmap yagmail python-dotenv
   ```
2. Set up your `.env` file with email credentials (see script for variable names).
3. Run:
   ```bash
   python task.py
   ```

## Requirements
- Python 3.x
- python-nmap
- yagmail
- python-dotenv
