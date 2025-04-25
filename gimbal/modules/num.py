import struct

# 设定 yaw, pitch, deep
yaw = 90
pitch = 0
deep = 95.2

# 组装数据包（Little Endian）
packet = struct.pack('<Bfff', 0x5A, yaw, pitch, deep)

# 打印十六进制
print("应发送的数据（Little Endian）:", packet.hex(), packet)

