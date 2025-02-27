# Auto Mining Script Malware

⚠️ Disclaimer

This script is for educational and research purposes only. It is intended to demonstrate how certain types of automation work, including how cryptocurrency miners like XMRig can be deployed and executed.

⚠️ WARNING: Using this script for unauthorized access, mining cryptocurrency on someone else's machine without explicit consent, or distributing malware is illegal and unethical. Misuse of this code may result in criminal charges and severe penalties. The authors take no responsibility for any misuse or harm caused by this script.


This script automates the process of downloading and setting up **XMRig** (a Monero mining software) on Windows, and it configures the software to run automatically on startup. It ensures that the script is executed with **Administrator** privileges, extracts the XMRig zip file, and sets up a **VBScript** to launch XMRig when the system starts.

## Overview
This Python script automates the following tasks:

- Downloads XMRig (a cryptocurrency miner for Monero).
- Extracts the downloaded ZIP file.
- Configures a startup script (VBScript) to run XMRig on system startup.
- Runs XMRig in the background.
- Optionally downloads and executes a sample file (like a game cheat for demonstration purposes).
- The script also checks for admin privileges and retrieves the public IP address to dynamically set up an extraction directory.



## Features

- Admin check: Ensures the script runs with administrative rights.
- Download and extraction: Automates the download and extraction of XMRig.
- Startup persistence: Creates a startup entry for automatic execution.
- IP-based directory creation: Organizes extracted files using the public IP.
- Silent execution: Option to hide console windows.

🛑 Legal Notice

This script is strictly for educational use. Running it on systems without permission violates computer crime laws. Always obtain explicit consent before testing or deploying any software.
