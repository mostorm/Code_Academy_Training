
# Day 7: SSH with Private Key

## Description
- `ssh_with_pkey.py`: Demonstrates SSH connection using a private key (Paramiko).

## How It Works
- Loads SSH credentials (hostname, port, username, private key path).
- Connects to the remote host using Paramiko and a private key.
- Prints connection status.

## How to Run
1. Install dependencies:
   ```bash
   pip install paramiko python-dotenv
   ```
2. Run:
   ```bash
   python ssh_with_pkey.py
   ```

## Requirements
- Python 3.x
- paramiko
- python-dotenv (if using .env files)
