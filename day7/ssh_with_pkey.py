import paramiko
import os
from dotenv import load_dotenv

load_dotenv()


def ssh_with_pkey(hostname, port, username, pkey_path):
    try:
        # Load the private key
        pkey = paramiko.RSAKey.from_private_key_file(pkey_path, password="mynameismohamed")
        # Create an SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the server using the private key
        ssh_client.connect(hostname=hostname, port=port, username=username, pkey=pkey)

        print(f"Successfully connected to {hostname} using private key authentication.")
        
        # You can execute commands here if needed
        # stdin, stdout, stderr = ssh_client.exec_command('ls -l')
        # print(stdout.read().decode())

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ssh_client.close()


if __name__ == "__main__":
    hostname = os.getenv("SSH_HOSTNAME")
    port = int(os.getenv("SSH_PORT", 22))
    username = os.getenv("SSH_USERNAME")
    pkey_path = os.getenv("SSH_PKEY_PATH")

    ssh_with_pkey(hostname, port, username, pkey_path)