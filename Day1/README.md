
# Day 1: IP Validator

## Description
This script (`ip_validator.py`) checks if the entered IP address is a valid IPv4 address using basic string and integer operations.

## How It Works
- Prompts the user to enter an IPv4 address.
- Splits the address into four parts and checks:
  - Each part is a number between 0 and 255.
  - No leading zeros are allowed.
- Prints whether the address is valid or not.

## How to Run
1. Open a terminal in this folder.
2. Run:
   ```bash
   python ip_validator.py
   ```
3. Enter an IPv4 address when prompted.

## Requirements
- Python 3.x (no external libraries needed)
