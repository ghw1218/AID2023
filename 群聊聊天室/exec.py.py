import os
from socket import *
import signal

HOST = '0.0.0.0'
POST = 8888
ADDR = (HOST, POST)

s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(ADDR)
s.listen(5)


def handle(c):
    while True:
        data = c.recv(1024)
        if not data:
            break
        print(data)
        c.send(b'OK')
    c.close()


signal.signal(signal.SIGINT, signal.SIG_IGN)
print("Listen in 8888.....")

while True:
    try:
        c, addr = s.accept()
        print("Connter from:", addr)
    except KeyboardInterrupt:
        os._exit(0)
    except Exception as e:
        print(e)
        continue

    pid = os.fork()
    if pid == 0:
        s.close()
        handle(c)
        os._exit(0)
    else:
        c.close()
