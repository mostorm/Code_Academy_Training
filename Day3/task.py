import re
import csv
import json
from collections import Counter

LOG_FILE = "firewall.log"
CSV_FILE = "output.csv"
JSON_FILE = "output.json"
THREAT_FILE = "threats.txt"

# Regex for realistic syslog-style firewall log
LOG_PATTERN = re.compile(
    r'^(?P<timestamp>\w{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2})\s+'
    r'(?P<host>\S+)\s+\S+:\s+'
    r'(?P<action>ACCEPT|DROP)\s+'
    r'(?P<protocol>TCP|UDP|ICMP)\s+'
    r'(?P<src_ip>(?:\d{1,3}\.){3}\d{1,3}):(?P<src_port>\d+)\s+->\s+'
    r'(?P<dst_ip>(?:\d{1,3}\.){3}\d{1,3}):(?P<dst_port>\d+)\s+'
    r'size=(?P<size>\d+)$'
)


def valid_ip(ip: str) -> bool:
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    return all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)


def parse_log_line(line: str):
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None

    entry = match.groupdict()

    # Validate IPs
    if not valid_ip(entry["src_ip"]) or not valid_ip(entry["dst_ip"]):
        return None

    # Convert numeric fields
    entry["src_port"] = int(entry["src_port"])
    entry["dst_port"] = int(entry["dst_port"])
    entry["size"] = int(entry["size"])

    # Keep only required fields
    return {
        "timestamp": entry["timestamp"],
        "action": entry["action"],
        "protocol": entry["protocol"],
        "src_ip": entry["src_ip"],
        "src_port": entry["src_port"],
        "dst_ip": entry["dst_ip"],
        "dst_port": entry["dst_port"],
        "size": entry["size"]
    }


def save_to_csv(entries, filename):
    if not entries:
        return

    fieldnames = list(entries[0].keys())
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)


def save_to_json(entries, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=4)


def save_threat_report(suspicious_ips, filename):
    with open(filename, "w", encoding="utf-8") as f:
        if suspicious_ips:
            f.write("Potential Threat Report\n")
            f.write("=======================\n")
            for ip, count in suspicious_ips.items():
                f.write(f"Source IP: {ip} appeared {count} times\n")
        else:
            f.write("No suspicious IPs detected.\n")


def main():
    parsed_entries = []
    malformed_count = 0

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            entry = parse_log_line(line)
            if entry:
                parsed_entries.append(entry)
            else:
                malformed_count += 1

    # Analysis
    action_counter = Counter(entry["action"] for entry in parsed_entries)
    dst_port_counter = Counter(entry["dst_port"] for entry in parsed_entries)
    src_ip_counter = Counter(entry["src_ip"] for entry in parsed_entries)

    top_3_ports = dst_port_counter.most_common(3)
    suspicious_ips = {ip: count for ip, count in src_ip_counter.items() if count >= 3}

    # Save outputs
    save_to_csv(parsed_entries, CSV_FILE)
    save_to_json(parsed_entries, JSON_FILE)
    save_threat_report(suspicious_ips, THREAT_FILE)

    # Print summary
    print("Firewall Log Analysis Complete")
    print("==============================")
    print(f"Valid entries: {len(parsed_entries)}")
    print(f"Malformed/skipped entries: {malformed_count}")
    print(f"ACCEPT count: {action_counter.get('ACCEPT', 0)}")
    print(f"DROP count: {action_counter.get('DROP', 0)}")

    print("\nTop 3 targeted destination ports:")
    for port, count in top_3_ports:
        print(f"Port {port}: {count} times")

    print("\nPotential threat IPs (appeared 3 or more times):")
    if suspicious_ips:
        for ip, count in suspicious_ips.items():
            print(f"{ip}: {count} times")
    else:
        print("None")

    print(f"\nSaved parsed entries to {CSV_FILE} and {JSON_FILE}")
    print(f"Saved threat report to {THREAT_FILE}")


if __name__ == "__main__":
    main()