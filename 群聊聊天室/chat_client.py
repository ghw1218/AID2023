"""
chat room客户端
发送请求,展示结果
"""
from socket import *
import os, sys

# 服务器地址
ADDR = ('192.168.0.195', 8088)


# 发送消息
def send_msg(s, name):
    while True:
        try:
            text = input("发言:")
        except KeyboardInterrupt:  # KeyboardInterrupt这个错误就相当于ctrl - c
            text = "quit"
        if text.strip() == "quit":
            msg = "Q" + name
            s.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天室")
        msg = 'C %s %s' % (name, text)
        s.sendto(msg.encode(), ADDR)


# 接收消息
def recv_msg(s):
    while True:
        try:
            data, addr = s.recvfrom(4096)
        except KeyboardInterrupt:
            sys.exit()
        # 从服务器收到EXIT退出
        if data.decode() == "EXIT":
            sys.exit()
        print(data.decode() + '\n发言:', end='')


# 客户端启动函数
def main():
    s = socket(AF_INET, SOCK_DGRAM)

    # 进入聊天室
    while True:
        name = input("请输入姓名:")
        msg = 'L ' + name
        s.sendto(msg.encode(), ADDR)
        # 接收反馈
        data, addr = s.recvfrom(128)
        if data.decode() == 'OK':
            print("您已经入聊天室")
            break
        else:
            print(data.decode())
    # 已经进入聊天室
    pid = os.fork()
    if pid < 0:
        sys.exit("Error!")
    elif pid == 0:
        send_msg(s, name)  # 子进程负责消息发送
    else:
        recv_msg(s)  # 父进程负责消息接收


main()
