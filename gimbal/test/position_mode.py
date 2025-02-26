import _thread
import time
from machine import Pin

class StepperMotor:
    def __init__(self, step_pin, dir_pin):
        """
        步进电机控制器
        :param step_pin: 脉冲引脚
        :param dir_pin: 方向引脚
        """
        self.motor_id = step_pin
        self.step_pin = Pin(step_pin, Pin.OUT)
        self.dir_pin = Pin(dir_pin, Pin.OUT)
        self.stop_flag = False
        self.active_thread = None

    def _step(self, steps, speed):
        """ 内部线程方法 """
        self.stop_flag = False
        self.dir_pin.value(1 if speed > 0 else 0)  # 根据速度符号设置方向
        speed = abs(speed)
        
        for i in range(steps):
            if self.stop_flag:
                print("控制指令被打断")
                break
            
            self.step_pin.on()
            time.sleep(0.5 / speed)
            self.step_pin.off()
            time.sleep(0.5 / speed)
        
            print(f"motor: {self.motor_id}, step: {i}, speed: {speed} Hz")

        self.active_thread = None

    def move(self, steps, speed):
        """
        非阻塞式移动
        :param steps: 步数（正负号表示方向）
        :param speed: 转速（Hz）
        """
        if self.active_thread:
            self.stop()
            
        self.active_thread = _thread.start_new_thread(
            self._step, (abs(steps), speed)
        )

    def stop(self):
        """ 立即停止运动 """
        print("stop now")
        if self.active_thread:
            self.stop_flag = True
            while self.active_thread:  # 等待线程退出
                time.sleep(0.01)

    def set_direction(self, clockwise=True):
        """ 设置运动方向 """
        self.dir_pin.value(1 if clockwise else 0)

# 使用示例
if __name__ == '__main__':
    motor_1 = StepperMotor(step_pin=25, dir_pin=27)
    motor_2 = StepperMotor(step_pin=26, dir_pin=16)
    
    # 正转100步，速度1Hz
    motor_1.move(10000, 5000)
    #motor_2.move(100, 10)
    time.sleep(3)
    
    # 反转200步，速度2Hz
    motor_1.move(-20000, 1000)
    time.sleep(3)
    motor_1.stop()