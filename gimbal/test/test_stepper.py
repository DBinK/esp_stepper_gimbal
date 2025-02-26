import time
from machine import Pin

led = Pin(2, Pin.OUT, value=1)

cnc_enable = Pin(12, Pin.OUT, value=0)

y_dir = Pin(17, Pin.OUT, value=0)
y_step = Pin(25, Pin.OUT, value=1)

while True :
    y_step.value(not y_step.value()) 
    led.value(not led.value())
    print("步进...")
    time.sleep(0.001)


