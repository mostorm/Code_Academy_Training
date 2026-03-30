def check_number(user_input):
    try:
        number=int(user_input)
        print(f"You entered the number: {number}")
        return number
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None

user_input=check_number(input("Enter a number: "))
 