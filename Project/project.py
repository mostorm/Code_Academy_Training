import paramiko
from datetime import datetime

SSH_HOSTNAME = "192.168.100.247"
SSH_PORT = 22
SSH_USERNAME = "codeacademy"
SSH_PKEY_PATH = r"C:\Users\Asus\Documents\python_course\.ssh\id_rsa"
#Remote config should be show-running-config these are mock examples
devices = [
    {"name": "router1", "hostname": SSH_HOSTNAME, "remote_config": "~/router1.conf"},  
    {"name": "router2", "hostname": SSH_HOSTNAME, "remote_config": "~/router2.conf"},
    {"name": "router3", "hostname": SSH_HOSTNAME, "remote_config": "~/router3.conf"},
]


def check_telnet(config: str) -> str:
    config_lower = config.lower()
    for line in config_lower.splitlines():
        if "transport input" in line and "telnet" in line:
            return "Telnet is enabled"
    return "Telnet is disabled"


def check_http_server(config: str) -> str:
    config_lower = config.lower()
    for line in config_lower.splitlines():
        if "ip http server" in line and "no ip http server" not in line:
            return "HTTP server is enabled"
    return "HTTP server is disabled"


def check_snmp(config: str) -> str:
    config_lower = config.lower()
    if "snmp-server community public" in config_lower or "snmp-server community private" in config_lower:
        return "Default SNMP community strings found"
    return "No default SNMP community strings found"


def ssh_with_pkey(hostname, port, username, pkey_path, remote_config):
    ssh_client = None
    try:
        pkey = paramiko.RSAKey.from_private_key_file(
            pkey_path,
            password="mynameismohamed"
        )

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh_client.connect(
            hostname=hostname,
            port=port,
            username=username,
            pkey=pkey
        )

        print(f"Successfully connected to {hostname} using private key authentication.")

        stdin, stdout, stderr = ssh_client.exec_command(f"cat {remote_config}")
        config = stdout.read().decode()
        error = stderr.read().decode().strip()

        if error:
            raise Exception(error)

        return config

    except Exception as e:
        raise Exception(f"An error occurred while connecting to {hostname}: {e}")

    finally:
        if ssh_client:
            ssh_client.close()


def audit_device(device, port, username, pkey_path):
    result = {
        "name": device["name"],
        "telnet": "Audit failed",
        "http": "Audit failed",
        "snmp": "Audit failed",
        "error": None,
    }

    try:
        config = ssh_with_pkey(
            device["hostname"],
            port,
            username,
            pkey_path,
            device["remote_config"]
        )

        result["telnet"] = check_telnet(config)
        result["http"] = check_http_server(config)
        result["snmp"] = check_snmp(config)

    except Exception as e:
        result["error"] = str(e)

    return result


def generate_report(results):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"Audit_Report_{today}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("--- Network Device Audit Report ---\n\n")

        for result in results:
            file.write(f"Device: {result['name']}\n")

            if result["error"]:
                file.write(f"- Error: {result['error']}\n\n")
                continue

            file.write(f"- Telnet Status: {result['telnet']}\n")
            file.write(f"- HTTP Server Status: {result['http']}\n")
            file.write(f"- SNMP Status: {result['snmp']}\n\n")

    return filename


def main():
    results = []

    for device in devices:
        results.append(audit_device(device, SSH_PORT, SSH_USERNAME, SSH_PKEY_PATH))

    report_file = generate_report(results)
    print(f"Audit report saved to {report_file}")


if __name__ == "__main__":
    main()