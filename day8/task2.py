from netmiko import ConnectHandler
import os
from datetime import datetime

# Device list using "ip" as required by the task
devices = [
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.1",
        "username": "admin",
        "password": "cisco",
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.2",
        "username": "admin",
        "password": "cisco",
    },
    {
        "device_type": "cisco_ios",
        "ip": "10.0.0.1",
        "username": "admin",
        "password": "cisco",
    },
    {
        "device_type": "juniper_junos",
        "ip": "192.168.1.3",
        "username": "admin",
        "password": "juniper",
    },
]

# Create backup directory
BACKUP_DIR = os.path.join(os.path.dirname(__file__), "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

for device in devices:
    ip = device["ip"]
    device_type = device["device_type"]

    print(f"Attempting to connect to {ip} ({device_type})...")

    net_connect = None

    try:
        # Connect to device
        net_connect = ConnectHandler(**device)
        print(f"Successfully connected to {ip}.")

        # Try enable mode for Cisco-like devices
        try:
            if "cisco" in device_type:
                net_connect.enable()
        except Exception:
            pass

        # Get hostname from prompt
        hostname = net_connect.find_prompt().replace("#", "").replace(">", "").strip()
        print(f"Device Hostname: {hostname}")
        print(f"Retrieving running configuration from {hostname}...")

        # Choose proper command based on vendor
        if "juniper" in device_type:
            config = net_connect.send_command("show configuration | display set")
        else:
            config = net_connect.send_command("show running-config")

        # Save config to file
        date_str = datetime.now().strftime("%Y-%m-%d")
        backup_filename = f"{hostname}_{date_str}.txt"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)

        with open(backup_path, "w", encoding="utf-8") as backup_file:
            backup_file.write(config)

        print(f"Configuration backup for {hostname} saved to ./backups/{backup_filename} successfully.")

    except Exception as e:
        print(f"Error backing up configuration for {ip}: {e}")

    finally:
        if net_connect:
            try:
                net_connect.disconnect()
            except Exception:
                pass
        print(f"Disconnected from {ip}.")