import time
import math

from machine import Pin, PWM, Timer


def test_timer(tim_callback):
    print(tim_callback)


# tim = Timer(-1)
# tim.init(period=200, mode=Timer.PERIODIC, callback=test_timer) 

# tim2 = Timer(-1)
# tim2.init(period=500, mode=Timer.PERIODIC, callback=test_timer) 

# tim3 = Timer(-1)
# tim3.init(period=100, mode=Timer.PERIODIC, callback=test_timer) 

# tim4 = Timer(-1)
# tim4.init(period=300, mode=Timer.PERIODIC, callback=test_timer) 

tim = Timer(0)
tim.init(period=200, mode=Timer.PERIODIC, callback=test_timer) 

tim2 = Timer(1)
tim2.init(period=500, mode=Timer.PERIODIC, callback=test_timer) 

tim3 = Timer(2)
tim3.init(period=100, mode=Timer.PERIODIC, callback=test_timer) 

tim4 = Timer(5)
tim4.init(period=300, mode=Timer.PERIODIC, callback=test_timer) 







