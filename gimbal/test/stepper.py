import time
import math
import _thread
from machine import Pin, PWM, Timer

class StepperMotor:
    def __init__(self, step_pin, dir_pin, min_speed=8, max_speed=500):
        """
        统一步进电机类，支持步数模式和速度模式（单一模式运行）
        :param step_pin: 脉冲引脚
        :param dir_pin: 方向引脚
        :param min_speed: 最小速度（适用于速度模式）
        :param max_speed: 最大速度（适用于速度模式）
        """
        # 公共属性
        self.motor_id = step_pin
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.dir_pin = Pin(dir_pin, Pin.OUT)

        # 速度模式属性
        self.pwm = PWM(self.step_pin, duty_u16=32768)
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.speed_mode = False  # 记录当前模式，避免冲突
        
        # 步数模式属性
        self.active_thread = None  # 仅用于步数模式
        self.stop_flag = False  # 控制步数模式的停止

    def move(self, steps, speed):
        """
        以固定步数移动（步数模式）
        :param steps: 运动步数（正负号决定方向）
        :param speed: 运动速度（Hz）
        """
        if self.speed_mode:
            raise RuntimeError("当前处于速度模式，无法使用步数模式")
        
        if self.active_thread:
            self.stop()
        
        self.stop_flag = False
        self.dir_pin.value(1 if speed > 0 else 0)
        speed = abs(speed)
        
        def _step_thread():
            for i in range(steps):
                if self.stop_flag:
                    print(f"motor {self.motor_id}: 停止")
                    break
                self.step_pin.on()
                time.sleep(0.5 / speed)
                self.step_pin.off()
                time.sleep(0.5 / speed)
                print(f"motor {self.motor_id}: step {i}, speed {speed} Hz")
            self.active_thread = None
        
        self.active_thread = _thread.start_new_thread(_step_thread, ())
    
    def rotate(self, speed):
        """
        以恒定速度旋转（速度模式）
        :param speed: 旋转速度（Hz），正负表示方向
        """
        if self.active_thread:
            raise RuntimeError("当前处于步数模式，无法使用速度模式")
        
        self.speed_mode = True
        self.dir_pin.value(1 if speed > 0 else 0)
        clamped_speed = max(self.min_speed, min(abs(speed), self.max_speed))
        self.pwm.duty_u16(32768)
        self.pwm.freq(clamped_speed)
        print(f"motor {self.motor_id}: 速度模式 {clamped_speed} Hz")

    def stop(self):
        """
        立即停止运动（适用于两种模式）
        """
        if self.active_thread:
            self.stop_flag = True
            while self.active_thread:
                time.sleep(0.01)
        
        if self.speed_mode:
            self.pwm.duty_u16(0)
            self.speed_mode = False
        print(f"motor {self.motor_id}: 停止")


class MultiMotorManager:
    def __init__(self, period=1, timer_id=-1):
        self.motors = []
        self.tim = Timer(timer_id)
        self.tim.init(period=period, mode=Timer.PERIODIC, callback=self._update_all)
    
    def add_motor(self, motor: StepperMotor):
        """注册电机到管理器（仅适用于速度模式）"""
        self.motors.append(motor)
    
    def _update_all(self, tim_callback):
        """定时器回调：更新所有电机速度"""
        for motor in self.motors:
            if motor.speed_mode:
                motor.rotate(motor.pwm.freq())  # 维持当前速度
        print("")  # 换行

# 使用示例
if __name__ == "__main__":
    motor1 = StepperMotor(step_pin=8, dir_pin=1)
    motor2 = StepperMotor(step_pin=9, dir_pin=2)
    
    # 测试步数模式
    motor1.move(100, 1)
    time.sleep(2)
    
    # 测试速度模式
    manager = MultiMotorManager(period=20, timer_id=-1)
    manager.add_motor(motor2)
    motor2.rotate(2)
    time.sleep(5)

    motor2.stop()
    motor1.stop()
