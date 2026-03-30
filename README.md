# Python and Networking Training Course

This repository contains a hands-on training course in Python and Networking.

## Current Repository Structure

```text
python_course/
├── Day1/
│   └── ip_validator.py
├── Day2/
│   └── test.py
└── README.md
```

## Course Structure

- Each day of training has its own folder (for example, `Day1`, `Day2`, etc.).
- Every day folder contains practical tasks and exercises.
- Tasks are designed to build skills step by step, from basics to more advanced topics.

## Goal

The goal of this course is to practice Python programming while applying it to networking-related problems and scenarios.

## How to Use This Repository

1. Open the folder for the current day.
2. Complete the tasks in order.
3. Test and improve your solutions.
4. Move to the next day folder when done.

## Current Day Files and Code

### Day1

File: `Day1/ip_validator.py`

```python
"""This function is an IP validator that checks if the entered IP address is a valid IPv4 address."""

def is_valid_ipv4(ipv4):
	# Split the IPv4 address into 4 parts
	ipsplit = ipv4.split(".")
    
	# Check if the length of the split parts is 4
	if len(ipsplit) != 4:
		return False
    
	for ip in ipsplit:
		# Check if each part is a digit
		if not ip.isdigit():
			return False
        
		number = int(ip)
        
		# Check if each part is between 0 and 255
		if number < 0 or number > 255:
			return False
        
		# Check if the string representation of the number matches the original part (to avoid leading zeros)
		if str(number) != ip:
			return False
            
	return True
#Prompt the user to Enter A valid IPv4 Address
ipv4=(input("enter an ipv4 Address: "))
is_valid = is_valid_ipv4(ipv4)

#print to the user that the ip is valid
if is_valid:
	print("Your IPv4 is valid")
#print to the user that the ip is not valid
else:
	print("The entered IP does not match the structure of IPv4") 

            
```

### Day2

File: `Day2/test.py`

```python
def check_number(user_input):
	try:
		number=int(user_input)
		print(f"You entered the number: {number}")
		return number
	except ValueError:
		print("Invalid input. Please enter a valid number.")
		return None

user_input=check_number(input("Enter a number: "))
```
