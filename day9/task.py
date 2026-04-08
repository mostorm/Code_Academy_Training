import nmap
import sys
import json
import yaml
import xmltodict
import yagmail
from dotenv import load_dotenv
import os

load_dotenv()
email = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")
to_email= os.getenv("EMAIL_TO")

def ping_scan(network):
    """
    Performs a ping scan on the given network and returns a list of live hosts.
    """
    print(f"[*] Scanning {network} for live hosts...")
    
    # 1. Create a PortScanner object
    nm = nmap.PortScanner()
    
    # 2. Run the scan
    #    -sn: Ping Scan - disables port scanning
    #    sudo: Nmap may need root privileges for some discovery techniques
    try:
        # For Linux/macOS, you might need 'sudo' for more effective scans
        # For Windows, run your script from an Administrator terminal
        nm.scan(hosts=network, arguments='-sn')
    except nmap.PortScannerError as e:
        print(f"Nmap error: {e}")
        print("\nMake sure you have Nmap installed and in your system's PATH.")
        print("You may also need to run this script with sudo/Administrator privileges.")
        sys.exit(1)

    # 3. Process the results
    live_hosts = []
    for host in nm.all_hosts():
        # Check if the host is reported as 'up'
        if nm[host].state() == 'up':
            print(f'[+] Host Found: {host}')
            live_hosts.append(host)
            
    return live_hosts

# --- Main Execution ---
if __name__ == "__main__":
    result_dict: dict = {}

    # Define the network to scan (e.g., your local network)
    target_network = '192.168.100.0/24' # Change this to your network
    
    hosts_found = ping_scan(target_network)
    result_dict['live_hosts'] = hosts_found

    # Save the results to a JSON file
    with open('.scan_results.json', 'w') as json_file:
        json.dump(result_dict, json_file, indent=4)
    print("\nScan results saved to './raw_ping_reports/scan_results.json'.")

    print("\n--- Scan Summary ---")
    if hosts_found:
        
        print(f"Total live hosts found: {len(hosts_found)}")
        for host in hosts_found:
            print(f" - {host}")
    else:
        print("No live hosts were found.")
    # Set the recipient email address
    yagmail.SMTP(email, password).send(
        to=to_email,
        subject="Nmap Scan Results Json file",
        contents="Please find the attached scan results.",
        attachments=".scan_results.json"
    )