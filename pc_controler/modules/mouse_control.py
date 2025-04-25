import time
from pynput import keyboard, mouse

import serial_send as ser

# 初始化前一个位置
last_x, last_y = None, None

switch = False

def on_move(x, y):
    global last_x, last_y
    if last_x is not None and last_y is not None:
        delta_x = x - last_x
        delta_y = y - last_y

        global switch
        
        if switch:
            print(f"Pointer moved to {x}, {y} with relative movement ({delta_x}, {delta_y})")
            ser.send_uart(delta_x, delta_y)

    last_x, last_y = x, y


def on_click(x, y, button, pressed):
    print(f"{'Pressed' if pressed else 'Released'} at {x}, {y} with {button}")
    if button == mouse.Button.right:
        global switch
        switch = not switch
        print(f"Switch: {switch}")

def on_scroll(x, y, dx, dy):
    print(f"Scrolled {'down' if dy < 0 else 'up'} at {x}, {y}")

# 启动鼠标监听
with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()
