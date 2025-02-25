# Auto Mining Script Malware

This script automates the process of downloading and setting up **XMRig** (a Monero mining software) on Windows, and it configures the software to run automatically on startup. It ensures that the script is executed with **Administrator** privileges, extracts the XMRig zip file, and sets up a **VBScript** to launch XMRig when the system starts.

## Features
- Downloads the latest version of XMRig for Windows.
- Extracts the downloaded zip file to a specified directory.
- Configures XMRig to start automatically on system boot using a VBScript.
- Runs XMRig in the background without showing a command window.
- Ensures the script is executed with Administrator privileges.

## Prerequisites
- Windows operating system.
- Administrator privileges to run the script.
- A valid **Monero wallet address** to mine to.

## How It Works
1. **Check for Admin Privileges**: The script checks if it is being run as an administrator. If not, it exits with a warning.
2. **Download XMRig**: The script downloads the latest XMRig release (v6.22.2) from the official GitHub repository.
3. **Extract XMRig**: It extracts the downloaded zip file to the specified directory.
4. **Configure Startup**: It creates a VBScript to launch XMRig on startup.
5. **Start Mining**: XMRig is launched with the specified configuration (Monero mining to a defined wallet address).

