""" Command-Line Subnet Calculator """
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from Day1.ip_validator import is_valid_ipv4
            

def calculate_subnet(ip, cidr):
    # Convert IP string to 32-bit integer
    octets = list(map(int, ip.split('.')))
    ip_int = (octets[0] << 24) + (octets[1] << 16) + (octets[2] << 8) + octets[3]
    
    # Calculate network and broadcast addresses
    mask = 0xFFFFFFFF << (32 - cidr)
    network_int = ip_int & mask
    broadcast_int = ip_int | (~mask & 0xFFFFFFFF)
    
    # Convert back to dotted decimal
    network_address = f"{(network_int >> 24) & 0xFF}.{(network_int >> 16) & 0xFF}.{(network_int >> 8) & 0xFF}.{network_int & 0xFF}"
    broadcast_address = f"{(broadcast_int >> 24) & 0xFF}.{(broadcast_int >> 16) & 0xFF}.{(broadcast_int >> 8) & 0xFF}.{broadcast_int & 0xFF}"
    
    usable_hosts = (2 ** (32 - cidr)) - 2
    return network_address, broadcast_address, usable_hosts
    
    


#     #network address
#     for i in range(4):
#         octets[i] = int(octets[i])
#     network_address = [0, 0, 0, 0]
#     for i in range(4):
#         if i < cidr // 8:
#             network_address[i] = octets[i]
#         elif i == cidr // 8:
#             network_address[i] = octets[i] & (0xFF << (8 - (cidr % 8)))
#         else:
#             network_address[i] = 0
#     #broadcast address
#     broadcast_address = [0, 0, 0, 0]
#     for i in range(4):
#         if i < cidr // 8:
#             broadcast_address[i] = octets[i]
#         elif i == cidr // 8:
#             broadcast_address[i] = octets[i] | (0xFF >> (cidr % 8))
#         else:
#             broadcast_address[i] = 255
#     #number of usable addresses
#     num_usable_addresses = (1 << (32 - cidr)) - 2
#     return network_address, broadcast_address, num_usable_addresses

# Prompt the user to enter an IP address and CIDR notation
ip = input("Enter an IPv4 address: ")
while not is_valid_ipv4(ip):
    print("Invalid IP address. Please enter a valid IPv4 address.")
    ip = input("Enter an IPv4 address: ")
cidr = input("Enter CIDR notation (e.g., 24): ")
while not cidr.isdigit() or not (0 <= int(cidr) <= 32) or  int(cidr)==str(cidr):
    print("Invalid CIDR notation. Please enter a valid CIDR notation (0-32).")
    cidr = input("Enter CIDR notation (e.g., 24): ")
cidr = int(cidr)
network_address, broadcast_address, num_usable_addresses = calculate_subnet(ip, cidr)
print("--subnet Calculator--")
print(f"Network Address: {network_address}")
print(f"Broadcast Address: {broadcast_address}")
print(f"Number of Usable Hosts: {num_usable_addresses}")
