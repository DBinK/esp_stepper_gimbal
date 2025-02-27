import time
from machine import Pin, PWM

led = Pin(2, Pin.OUT, value=1)

y_dir = Pin(27, Pin.OUT, value=0)
y_step = Pin(25, Pin.OUT, value=0)
y_pwm = PWM(y_step, duty_u16=32768)

x_dir = Pin(16, Pin.OUT, value=0)
x_step = Pin(26, Pin.OUT, value=0)
x_pwm = PWM(x_step, duty_u16=32768)

y_pwm.freq(300)
x_pwm.freq(300)

time.sleep(5)

y_pwm.freq(500)

time.sleep(5)

y_pwm.freq(800)

time.sleep(5)


# while True :
#     
#     led.value(not led.value())
#     print("步进...")
#     time.sleep(0.0005)



