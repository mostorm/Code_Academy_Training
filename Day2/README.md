
# Day 2: Subnet Calculator & Input Validation

## Description
- `Command-Line Subnet Calculator.py`: Calculates network and broadcast addresses and usable hosts for a given IPv4/CIDR.
- `test.py`: Simple script to validate number input.

## How They Work
- **Subnet Calculator**:
  - Prompts for an IP and CIDR.
  - Validates the IP using the Day 1 validator.
  - Calculates network address, broadcast address, and number of usable hosts.
  - Prints the results.
- **test.py**:
  - Prompts for a number and checks if the input is valid.

## How to Run
1. Open a terminal in this folder.
2. For the subnet calculator:
   ```bash
   python "Command-Line Subnet Calculator.py"
   ```
3. For the test script:
   ```bash
   python test.py
   ```

## Requirements
- Python 3.x
