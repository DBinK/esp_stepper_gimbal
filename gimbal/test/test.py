
import time

from modules.stepper import Stepper
from modules.serial_recv import read_uart

motor_y = Stepper(25,27,steps_per_rev=200*16,speed_sps=1000, timer_id=1)
motor_x = Stepper(26,16,steps_per_rev=200*16,speed_sps=1000, timer_id=2)

while True:
    data = read_uart()
    
    if data[0] == 1:
        motor_x.target_deg_relative(-data[1])
    
    if data:
        print(data)

    time.sleep(0.01)