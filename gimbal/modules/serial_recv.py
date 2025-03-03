import re
import time
from machine import Pin, UART

uart = UART(1, baudrate=115200, tx=4, rx=2)

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
    data = [0, 0, 0]
    if uart.any():
        try:
            msg = uart.readline()
            if not msg:  # 处理空消息
                return [0, 0, 0]
            msg_str = msg.decode('utf-8').strip()  # 安全解码
            print(f"接收到原始数据：{msg_str}")  # 调试输出
            data = parse_string(msg_str)
        except UnicodeDecodeError:
            print(f"解码错误：无法解析字节数据 {msg}")
        except Exception as e:
            print(f"未知错误：{e}")
    return data

if __name__ == "__main__":
    print("正在读取uart数据...")
    while True:
        data = read_uart()
        if data[0] == 1:  # 仅处理有效数据
            print(f"成功解析数据：{data[1:]}")
        time.sleep(0.1)