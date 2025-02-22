import os
import tarfile
import subprocess
import requests

URL = "https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-linux-static-x64.tar.gz"
FILENAME = "xmrig-6.22.2-linux-static-x64.tar.gz"
EXTRACTED_DIR = "xmrig-6.22.2"
print("Made by Cr0mb")
print("\n     XMRIG INSTALLER")
xmr_wallet = input("Enter your XMR wallet address: ")
if not xmr_wallet:
    print("Wallet address is required.")
    exit(1)

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
    "-u", xmr_wallet,
    "--tls", "--coin", "monero"
])
