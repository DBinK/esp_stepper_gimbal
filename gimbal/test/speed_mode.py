import time
import math
from machine import Pin, PWM, Timer

class StepperMotor:
    def __init__(self, step_pin, dir_pin=1, min_speed=8, max_speed=500000):
        self.motor_id = step_pin
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.pwm = PWM(self.step_pin, duty_u16=32768)
        self.speed = 0
        self.min_speed = min_speed
        self.max_speed = max_speed
        
    def _update(self):
        """由管理器调用的内部更新方法"""
        if abs(self.speed) < abs(self.min_speed):
            self.pwm.duty_u16(0)
            # print(f" {self.motor_id}_speed: 速度太小", end= " | ")
        else:
            self.dir_pin.value(1 if self.speed > 0 else 0)
            clamped_speed = int(max(self.min_speed, min(abs(self.speed), self.max_speed)))
            self.pwm.duty_u16(32768)
            self.pwm.freq(clamped_speed)

            print(f" {self.motor_id}_speed: {clamped_speed} Hz", end= " | ")

    def stop(self):
        self.pwm.duty_u16(0)
        self.speed = 0

    def set_set_direction(self, clockwise=True):
        self.dir_pin.value(1 if clockwise else 0)


class MultiMotorManager:
    def __init__(self, period=1, timer_id=-1):
        self.motors = []
        self.tim = Timer(timer_id)
        self.tim.init(period=period, mode=Timer.PERIODIC, callback=self._update_all)
    
    def add_motor(self, motor: StepperMotor):
        """注册电机到管理器"""
        self.motors.append(motor)
    
    def _update_all(self, tim_callback):
        """定时器回调：更新所有注册的电机"""
        for motor in self.motors:
            motor._update()

        print("")  # 换行

# 使用示例
if __name__ == "__main__":
    # 创建管理器（共享定时器）
    manager = MultiMotorManager(period=20, timer_id=-1)
    
    # 创建多个电机并注册到管理器
    motor1 = StepperMotor(step_pin=25, dir_pin=27)
    motor2 = StepperMotor(step_pin=26, dir_pin=16)
    manager.add_motor(motor1)
    manager.add_motor(motor2)
    
    motor1.speed = 4000
    time.sleep(5)
    motor1.speed = -8000
    time.sleep(9)
    
    try:
        for i in range(100000):
            # 两个电机不同速度曲线
            AMP = 500
            speed1 = int(math.sin(i/50) * AMP + AMP)
            speed2 = int(math.cos(i/3) * AMP + AMP)
            motor1.speed = speed1
            motor2.speed = speed2
            time.sleep(0.02)
            
    except KeyboardInterrupt:
        motor1.stop()
        motor2.stop()