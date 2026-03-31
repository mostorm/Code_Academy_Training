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
# #Prompt the user to Enter A valid IPv4 Address
# ipv4=(input("enter an ipv4 Address: "))
# is_valid = is_valid_ipv4(ipv4)

# #print to the user that the ip is valid
# if is_valid:
#     print("Your IPv4 is valid")
# #print to the user that the ip is not valid
# else:
#     print("The entered IP does not match the structure of IPv4") 

            

