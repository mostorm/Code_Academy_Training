# Day 6: Network Automation - Task & Solution

## Task: Automated Configuration Backup

**Problem Statement:**

Develop a Python script that automates the process of backing up the running configuration from a list of network devices. The script should connect to each device, retrieve its running configuration, and save it to a local file. Each backup file must be uniquely named using the device's hostname and the current date (e.g., `router1_2026-02-26.txt`). The script should also gracefully handle potential connection errors for unreachable devices.

**Requirements:**

*   Use the `netmiko` library for device connectivity and command execution.
*   Accept a list of device dictionaries, each containing `device_type`, `ip`, `username`, and `password`.
*   For each device, connect, retrieve the running configuration, and disconnect.
*   Name the backup file using the format: `<hostname>_<YYYY-MM-DD>.txt`.
*   Implement error handling for connection failures.
*   Print status messages indicating success or failure for each device.


## Sample Outputs

### Sample Output 1: Successful Backup for Multiple Devices

*(Assuming `192.168.1.1` and `192.168.1.2` are reachable and `10.0.0.1` is unreachable, and `192.168.1.3` is a Juniper device with correct credentials)*

```text

Attempting to connect to 192.168.1.1 (cisco_ios)...
Successfully connected to 192.168.1.1.
Device Hostname: router1
Retrieving running configuration from router1...
Configuration backup for router1 saved to ./backups/router1_2026-02-26.txt successfully.
Disconnected from 192.168.1.1.

Attempting to connect to 192.168.1.2 (cisco_ios)...
Successfully connected to 192.168.1.2.
Device Hostname: switch1
Retrieving running configuration from switch1...
Configuration backup for switch1 saved to ./backups/switch1_2026-02-26.txt successfully.
Disconnected from 192.168.1.2.

Attempting to connect to 10.0.0.1 (cisco_ios)...
Error backing up configuration for 10.0.0.1: Timed out trying to connect to 10.0.0.1
Disconnected from 10.0.0.1.

Attempting to connect to 192.168.1.3 (juniper_junos)...
Successfully connected to 192.168.1.3.
Device Hostname: juniper_router
Retrieving running configuration from juniper_router...
Configuration backup for juniper_router saved to ./backups/juniper_router_2026-02-26.txt successfully.
Disconnected from 192.168.1.3.
```

### Sample Output 2: All Devices Unreachable

*(Assuming all devices in `my_devices` are unreachable)*

```text

Attempting to connect to 192.168.1.1 (cisco_ios)...
Error backing up configuration for 192.168.1.1: Timed out trying to connect to 192.168.1.1
Disconnected from 192.168.1.1.

Attempting to connect to 192.168.1.2 (cisco_ios)...
Error backing up configuration for 192.168.1.2: Timed out trying to connect to 192.168.1.2
Disconnected from 192.168.1.2.

Attempting to connect to 10.0.0.1 (cisco_ios)...
Error backing up configuration for 10.0.0.1: Timed out trying to connect to 10.0.0.1
Disconnected from 10.0.0.1.

Attempting to connect to 192.168.1.3 (juniper_junos)...
Error backing up configuration for 192.168.1.3: Timed out trying to connect to 192.168.1.3
Disconnected from 192.168.1.3.
```

## Solution Logic Flowchart

```text
Start Script
    |
    V
Initialize Device List, Username, Password
    |
    V
Loop Through Each Device in List
    |
    V
Extract IP and Device Type
    |
    V
Initialize net_connect to None
    |
    V
Try to Connect to Device
    |-- Success --> Get Hostname
    |                 |
    |                 V
    |               Get Current Date
    |                 |
    |                 V
    |               Construct Backup Filename and Path
    |                 |
    |                 V
    |               Ensure Backup Directory Exists
    |                 |
    |                 V
    |               Retrieve Running Configuration
    |                 |
    |                 V
    |               Write Config to File
    |                 |
    |                 V
    |               Print Success Message
    |                 |
    V                 V
Disconnect from Device
    |
    |-- Failure --> Print Error Message
    |                 |
    V                 V
Loop to Next Device (if any)
    |
    V
End Script
```

*(Note: In a real-world scenario, a high-quality graphic illustration (e.g., `day6_task_flowchart.png`) would be embedded here to visually explain the solution logic. Due to technical limitations in rendering complex diagrams, a text-based representation is provided.)

**Figure 6.2: Configuration Backup Script Logic**

This flowchart illustrates the logical flow of the automated configuration backup script. It details the steps from initializing device information, iterating through each device, establishing a connection, retrieving and saving the configuration, and handling disconnections and errors.# Day 6: Network Automation - Task & Solution

## Task: Automated Configuration Backup

**Problem Statement:**

Develop a Python script that automates the process of backing up the running configuration from a list of network devices. The script should connect to each device, retrieve its running configuration, and save it to a local file. Each backup file must be uniquely named using the device's hostname and the current date (e.g., `router1_2026-02-26.txt`). The script should also gracefully handle potential connection errors for unreachable devices.

**Requirements:**

*   Use the `netmiko` library for device connectivity and command execution.
*   Accept a list of device dictionaries, each containing `device_type`, `ip`, `username`, and `password`.
*   For each device, connect, retrieve the running configuration, and disconnect.
*   Name the backup file using the format: `<hostname>_<YYYY-MM-DD>.txt`.
*   Implement error handling for connection failures.
*   Print status messages indicating success or failure for each device.


## Sample Outputs

### Sample Output 1: Successful Backup for Multiple Devices

*(Assuming `192.168.1.1` and `192.168.1.2` are reachable and `10.0.0.1` is unreachable, and `192.168.1.3` is a Juniper device with correct credentials)*

```text

Attempting to connect to 192.168.1.1 (cisco_ios)...
Successfully connected to 192.168.1.1.
Device Hostname: router1
Retrieving running configuration from router1...
Configuration backup for router1 saved to ./backups/router1_2026-02-26.txt successfully.
Disconnected from 192.168.1.1.

Attempting to connect to 192.168.1.2 (cisco_ios)...
Successfully connected to 192.168.1.2.
Device Hostname: switch1
Retrieving running configuration from switch1...
Configuration backup for switch1 saved to ./backups/switch1_2026-02-26.txt successfully.
Disconnected from 192.168.1.2.

Attempting to connect to 10.0.0.1 (cisco_ios)...
Error backing up configuration for 10.0.0.1: Timed out trying to connect to 10.0.0.1
Disconnected from 10.0.0.1.

Attempting to connect to 192.168.1.3 (juniper_junos)...
Successfully connected to 192.168.1.3.
Device Hostname: juniper_router
Retrieving running configuration from juniper_router...
Configuration backup for juniper_router saved to ./backups/juniper_router_2026-02-26.txt successfully.
Disconnected from 192.168.1.3.
```

### Sample Output 2: All Devices Unreachable

*(Assuming all devices in `my_devices` are unreachable)*

```text

Attempting to connect to 192.168.1.1 (cisco_ios)...
Error backing up configuration for 192.168.1.1: Timed out trying to connect to 192.168.1.1
Disconnected from 192.168.1.1.

Attempting to connect to 192.168.1.2 (cisco_ios)...
Error backing up configuration for 192.168.1.2: Timed out trying to connect to 192.168.1.2
Disconnected from 192.168.1.2.

Attempting to connect to 10.0.0.1 (cisco_ios)...
Error backing up configuration for 10.0.0.1: Timed out trying to connect to 10.0.0.1
Disconnected from 10.0.0.1.

Attempting to connect to 192.168.1.3 (juniper_junos)...
Error backing up configuration for 192.168.1.3: Timed out trying to connect to 192.168.1.3
Disconnected from 192.168.1.3.
```

## Solution Logic Flowchart

```text
Start Script
    |
    V
Initialize Device List, Username, Password
    |
    V
Loop Through Each Device in List
    |
    V
Extract IP and Device Type
    |
    V
Initialize net_connect to None
    |
    V
Try to Connect to Device
    |-- Success --> Get Hostname
    |                 |
    |                 V
    |               Get Current Date
    |                 |
    |                 V
    |               Construct Backup Filename and Path
    |                 |
    |                 V
    |               Ensure Backup Directory Exists
    |                 |
    |                 V
    |               Retrieve Running Configuration
    |                 |
    |                 V
    |               Write Config to File
    |                 |
    |                 V
    |               Print Success Message
    |                 |
    V                 V
Disconnect from Device
    |
    |-- Failure --> Print Error Message
    |                 |
    V                 V
Loop to Next Device (if any)
    |
    V
End Script
```

*(Note: In a real-world scenario, a high-quality graphic illustration (e.g., `day6_task_flowchart.png`) would be embedded here to visually explain the solution logic. Due to technical limitations in rendering complex diagrams, a text-based representation is provided.)

**Figure 6.2: Configuration Backup Script Logic**

This flowchart illustrates the logical flow of the automated configuration backup script. It details the steps from initializing device information, iterating through each device, establishing a connection, retrieving and saving the configuration, and handling disconnections and errors.# Day 6: Network Automation - Task & Solution

## Task: Automated Configuration Backup

**Problem Statement:**

Develop a Python script that automates the process of backing up the running configuration from a list of network devices. The script should connect to each device, retrieve its running configuration, and save it to a local file. Each backup file must be uniquely named using the device's hostname and the current date (e.g., `router1_2026-02-26.txt`). The script should also gracefully handle potential connection errors for unreachable devices.

**Requirements:**

*   Use the `netmiko` library for device connectivity and command execution.
*   Accept a list of device dictionaries, each containing `device_type`, `ip`, `username`, and `password`.
*   For each device, connect, retrieve the running configuration, and disconnect.
*   Name the backup file using the format: `<hostname>_<YYYY-MM-DD>.txt`.
*   Implement error handling for connection failures.
*   Print status messages indicating success or failure for each device.


## Sample Outputs

### Sample Output 1: Successful Backup for Multiple Devices

*(Assuming `192.168.1.1` and `192.168.1.2` are reachable and `10.0.0.1` is unreachable, and `192.168.1.3` is a Juniper device with correct credentials)*

```text

Attempting to connect to 192.168.1.1 (cisco_ios)...
Successfully connected to 192.168.1.1.
Device Hostname: router1
Retrieving running configuration from router1...
Configuration backup for router1 saved to ./backups/router1_2026-02-26.txt successfully.
Disconnected from 192.168.1.1.

Attempting to connect to 192.168.1.2 (cisco_ios)...
Successfully connected to 192.168.1.2.
Device Hostname: switch1
Retrieving running configuration from switch1...
Configuration backup for switch1 saved to ./backups/switch1_2026-02-26.txt successfully.
Disconnected from 192.168.1.2.

Attempting to connect to 10.0.0.1 (cisco_ios)...
Error backing up configuration for 10.0.0.1: Timed out trying to connect to 10.0.0.1
Disconnected from 10.0.0.1.

Attempting to connect to 192.168.1.3 (juniper_junos)...
Successfully connected to 192.168.1.3.
Device Hostname: juniper_router
Retrieving running configuration from juniper_router...
Configuration backup for juniper_router saved to ./backups/juniper_router_2026-02-26.txt successfully.
Disconnected from 192.168.1.3.
```

### Sample Output 2: All Devices Unreachable

*(Assuming all devices in `my_devices` are unreachable)*

```text

Attempting to connect to 192.168.1.1 (cisco_ios)...
Error backing up configuration for 192.168.1.1: Timed out trying to connect to 192.168.1.1
Disconnected from 192.168.1.1.

Attempting to connect to 192.168.1.2 (cisco_ios)...
Error backing up configuration for 192.168.1.2: Timed out trying to connect to 192.168.1.2
Disconnected from 192.168.1.2.

Attempting to connect to 10.0.0.1 (cisco_ios)...
Error backing up configuration for 10.0.0.1: Timed out trying to connect to 10.0.0.1
Disconnected from 10.0.0.1.

Attempting to connect to 192.168.1.3 (juniper_junos)...
Error backing up configuration for 192.168.1.3: Timed out trying to connect to 192.168.1.3
Disconnected from 192.168.1.3.
```

## Solution Logic Flowchart

```text
Start Script
    |
    V
Initialize Device List, Username, Password
    |
    V
Loop Through Each Device in List
    |
    V
Extract IP and Device Type
    |
    V
Initialize net_connect to None
    |
    V
Try to Connect to Device
    |-- Success --> Get Hostname
    |                 |
    |                 V
    |               Get Current Date
    |                 |
    |                 V
    |               Construct Backup Filename and Path
    |                 |
    |                 V
    |               Ensure Backup Directory Exists
    |                 |
    |                 V
    |               Retrieve Running Configuration
    |                 |
    |                 V
    |               Write Config to File
    |                 |
    |                 V
    |               Print Success Message
    |                 |
    V                 V
Disconnect from Device
    |
    |-- Failure --> Print Error Message
    |                 |
    V                 V
Loop to Next Device (if any)
    |
    V
End Script
```

*(Note: In a real-world scenario, a high-quality graphic illustration (e.g., `day6_task_flowchart.png`) would be embedded here to visually explain the solution logic. Due to technical limitations in rendering complex diagrams, a text-based representation is provided.)

**Figure 6.2: Configuration Backup Script Logic**

This flowchart illustrates the logical flow of the automated configuration backup script. It details the steps from initializing device information, iterating through each device, establishing a connection, retrieving and saving the configuration, and handling disconnections and errors.