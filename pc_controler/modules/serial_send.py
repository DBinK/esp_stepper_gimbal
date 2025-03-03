import time
import serial 

# 初始化 串口
ser = serial.Serial('COM6', 115200, timeout=0.1)

def send_uart(x, y):

    data = f"pad:{x},{y}\n"

    ser.write(data.encode("utf-8"))


if __name__ == "__main__":
    print("正在发送uart数据...")
    i = -1
    while True:
        x = 90*i
        y = 90*i
        send_uart(x, y)
        print(ser.readline().decode("utf-8"))
        i *= -1
        time.sleep(2)