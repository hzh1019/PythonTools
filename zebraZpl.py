import socket

# 创建一个套接字对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到打印机
s.connect(('10.200.37.8', 9100))

# 发送ZPL命令
s.send(b'^XA^HH^XZ')

# 接收返回的数据
data = s.recv(1024)

# 打印返回的数据
print(data)

# 关闭套接字
s.close()
