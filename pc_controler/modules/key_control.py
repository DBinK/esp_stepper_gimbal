import time
from pynput import keyboard

def on_press(key):
    try:
        print(f"Key {key.char} was pressed")
        
        if key.char == 'w':
            print("Forward")
        
        elif key.char == 's':
            print("Backward")
        
        elif key.char == 'a':
            print("Left")

        elif key.char == 'd':
            print("Right")
            
    except AttributeError:
        print(f"Special key {key} was pressed")

def on_release(key):
    try:
        print(f"Key {key.char} was released")
        
        if key.char == 'w':
            print("Stop Forward")
        
        elif key.char == 's':
            print("Stop Backward")
        
        elif key.char == 'a':
            print("Stop Left")

        elif key.char == 'd':
            print("Stop Right")
            
    except AttributeError:
        print(f"Special key {key} was released")

    # 停止监听
    if key == keyboard.Key.esc:
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()