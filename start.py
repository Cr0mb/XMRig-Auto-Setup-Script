import os
import tarfile
import subprocess
import requests

URL = "https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-linux-static-x64.tar.gz"
FILENAME = "xmrig-6.22.2-linux-static-x64.tar.gz"
EXTRACTED_DIR = "xmrig-6.22.2"
BITCOIN_ADDRESS = "82WFpBT3pLrBHDHXpe5TL2cQLEepYDieiDMZADyb3pHLd8oQCrMLs44WCi8vBN3aT8AkbRXnhry5JFEdyS9nzWSP6jDNWn1"

print("Made by Cr0mb")
print("\n     XMRIG INSTALLER")

print("Downloading XMRig...")
response = requests.get(URL, stream=True)
with open(FILENAME, "wb") as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
print("Download complete.")

print("Extracting XMRig...")
with tarfile.open(FILENAME, "r:gz") as tar:
    tar.extractall()
print("Extraction complete.")

os.chdir(EXTRACTED_DIR)
print("Starting XMRig...")
subprocess.run([
    "./xmrig",
    "-o", "xmr-us-east1.nanopool.org:14433",
    "-u", BITCOIN_ADDRESS,
    "--tls", "--coin", "monero"
])
