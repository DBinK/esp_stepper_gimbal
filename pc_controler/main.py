import time
from pynput import keyboard

import modules.serial_send as ser

def on_press(key):
    try:
        print(f"Key {key.char} was pressed")
        
        if key.char == 'w':
            print("Forward")
            ser.send_uart(0, -10)
        
        elif key.char == 's':
            print("Backward")
            ser.send_uart(0, 10)
        
        elif key.char == 'a':
            print("Left")
            ser.send_uart(-10, 0)

        elif key.char == 'd':
            print("Right")
            ser.send_uart(10, 0)
            
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