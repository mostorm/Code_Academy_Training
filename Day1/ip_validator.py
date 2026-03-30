#Prompt the user to Enter A valid IPv4 Address
ipv4=(input("enter an ipv4 Address: "))
#Spliting the IPv4 entered into 4 parts
ipsplit=ipv4.split(".")
#Condition for checking if the ip is valid 
condition=True
#If Statement for checking the lenth of the entered ip
if not (len(ipsplit)==4):
    condition=False

# for loop to check each number
for ip in ipsplit:
    #If statement to check if ach number is a digit number
    if not ip.isdigit():
        condition=False
    number=int(ip)
    #If Statement to check if the number enetered for each part is between 0 and 255
    if number<0 or number>255:
        condition=False
#print to the user that the ip is valid
if (condition==True):
    print("Your IPv4 is valid")
#print to the user that the ip is not valid
else:
    print("The entered IP does not match the structure of IPv4") 

            

