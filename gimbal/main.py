import time
import network
import _thread 
from machine import Pin

from modules.utils import TimeDiff
from modules.now_recv import read_espnow, process_data
# from modules.speed_mode import StepperMotor, MultiMotorManager
# from modules.position_mode import StepperMotor
from modules.stepper import Stepper

time.sleep(1)  # 防止点停止按钮后马上再启动导致 Thonny 连接不上

imu_dt = TimeDiff()
rc_dt  = TimeDiff()

# # 创建管理器（共享定时器）
# manager = MultiMotorManager(period=2, timer_id=-1)

# # 创建多个电机并注册到管理器
# motor_y = StepperMotor(step_pin=26, dir_pin=16)
# motor_x = StepperMotor(step_pin=25, dir_pin=27)
# manager.add_motor(motor_x)
# manager.add_motor(motor_y)

# motor_x = StepperMotor(step_pin=25, dir_pin=27)
# motor_y = StepperMotor(step_pin=26, dir_pin=16)

motor_x = Stepper(25,27,steps_per_rev=200*16,speed_sps=5000, timer_id=1)
motor_y = Stepper(26,16,steps_per_rev=200*16,speed_sps=5000, timer_id=2)

motor_x.target_deg(90)
motor_y.target_deg(45)
time.sleep(3.0)

motor_x.target_deg(0)
motor_y.target_deg(0)
time.sleep(3.0)

motor_x.target_deg_relative(90)
time.sleep(3.0)
motor_x.target_deg_relative(-180)
time.sleep(3.0)

# 摇杆数据全局变量
rc_data = [0, 0, 0, 0, 0, 0, 0, 0]
stick_work = False

def rc_loop():
    
    global rc_data, stick_work

    while True:
        time.sleep(0.01)
        # time.sleep(0.001)

        ms = rc_dt.time_diff() / 1_000_000
        Hz = int(1/(ms/1000)) # if ms > 0.0001 else 0

        print(f"rc_loop() 循环时间: {ms:.3f}ms, 频率: {Hz}Hz")

        data, stick_work = read_espnow()
        rc_data = process_data(data)

def gimbal_loop():
    
    global rc_data, stick_work

    while True:
        # time.sleep(0.1)
        time.sleep(0.001)

        ms = imu_dt.time_diff() / 1_000_000
        Hz = int(1/(ms/1000)) # if ms > 0.0001 else 0

        print(f"imu_loop() 循环时间: {ms:.3f}ms, 频率: {Hz}Hz")
        print(f"rc_data: {rc_data}")

        # 获取摇杆数据
        if stick_work:
            _ly = rc_data[1]
            _lx = rc_data[2]
            _rx = rc_data[3]
            _ry = rc_data[4]
        
            if rc_data[6] != 0x0:  # 急停保险
                motor_x.speed = 0
                motor_y.speed = 0
                rc_data = [0, 0, 0, 0, 0, 0, 0, 0]
                print("急停!")
                time.sleep(5)

            # 摇杆数据缩放
            y_speed = _ry * 0.1
            x_speed = _lx * 0.1

            print(f"x_speed: {x_speed}, y_speed: {y_speed}")

            # 控制电机
            # motor_x.speed = x_speed
            # motor_y.speed = y_speed
            
            motor_x.target_deg_relative(x_speed)
            motor_y.target_deg_relative(y_speed)

        else:  # 摇杆数据为空
            print("摇杆数据为空!")
            # motor_x.speed = 0
            # motor_y.speed = 0
            motor_x.stop()
            motor_y.stop()


# 创建两个线程
_thread.start_new_thread(rc_loop, ())   # 创建一个线程，执行 rc_loop() 函数
_thread.start_new_thread(gimbal_loop, ())  # 创建一个线程，执行 imu_loop() 函数

