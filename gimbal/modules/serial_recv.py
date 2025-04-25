import re
import time
import struct
from machine import Pin, UART

uart = UART(1, baudrate=115200, tx=18, rx=19)

def parse_string(s):
    """
    解析形如 'pad:<num1>,<num2>' 的字符串，返回两个整数。
    
    参数:
        s (str): 输入字符串
    
    返回:
        list: 包含三个元素的列表 [status, num1, num2]
              status=1表示成功，0表示失败
    
    异常处理:
        捕获所有格式错误并返回明确的错误信息
    """
    # 检查前缀是否为 'pad:'
    if not s.startswith('pad:'):
        print(f"格式错误：字符串必须以 'pad:' 开头（输入：{s}）")
        return [0, 0, 0]
    
    # 分割剩余部分
    parts = s[len('pad:'):].split(',')
    parts = [p.strip() for p in parts]  # 去除空格
    
    # 检查参数数量
    if len(parts) != 2:
        print(f"参数数量错误：需要 2 个参数，实际收到 {len(parts)} 个（输入：{s}）")
        return [0, 0, 0]
    
    # 验证数字格式
    try:
        num1 = int(parts[0])
        num2 = int(parts[1])
        return [1, num1, num2]
    
    except ValueError:
        # 安全地确定无效参数
        invalid = []
        for part in parts:
            if not part.lstrip('-').isdigit():
                invalid.append(part)
        
        if invalid:
            print(f"无效参数：'{invalid[0]}' 不是整数（输入：{s}）")
        else:
            print(f"未知转换错误（输入：{s}）")
        
        return [0, 0, 0]

def read_uart():
    """
    从 UART 读取数据并解析 32 位浮点数 (yaw, pitch, deep)
    数据格式：
    | 0xA5 (1 byte) | yaw (4 bytes) | pitch (4 bytes) | deep (4 bytes) |
    """
    while uart.any() < 13:  # 确保至少 13 字节
        time.sleep(0.01)  # 等待数据到齐

    raw_data = uart.read(256)  # 读取 13 字节
    print(f"收到数据包: {raw_data.hex()}")
    
    if raw_data[0] != 0x5A:
        print(f"无效数据包，丢弃")
        return [0, 0, 0, 0]

    try:
        yaw, pitch, deep = struct.unpack('<fff', raw_data[1:])  # 解析浮点数
        raw_data = []
        return [1, yaw, pitch, deep]
    
    except struct.error:
        print("数据解析错误")
        return [0, 0, 0, 0]
    
if __name__ == "__main__":
    print("正在读取 UART 数据...")
    while True:
        data = read_uart()
        if data[0] == 1:
            print(f"成功解析数据：yaw={data[1]:.2f}, pitch={data[2]:.2f}, deep={data[3]:.2f}")
        time.sleep(0.1)
        

