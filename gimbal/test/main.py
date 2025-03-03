from modules.stepper import Stepper
import time

s2 = Stepper(25,27,steps_per_rev=200*16,speed_sps=1000, timer_id=1)
s1 = Stepper(26,16,steps_per_rev=200*16,speed_sps=1000, timer_id=2)
# some boards might require a different timer_id for each stepper:
# s1 = Stepper(18,19,steps_per_rev=200,speed_sps=50,timer_id=0)
# s2 = Stepper(20,21,steps_per_rev=200,speed_sps=50,timer_id=1)

while True:
    s1.target_deg_relative(-90)
    s2.target_deg(90)
    time.sleep(2.0)

    s1.target_deg_relative(90)
    s2.target_deg(0)
    time.sleep(2.0)
