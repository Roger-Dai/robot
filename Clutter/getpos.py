import socket
from time import sleep

HOST = '140.233.20.115'
PORT = 30000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', PORT))

s.listen(5)
temp = s.accept()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = temp[0]
client_addr = temp[1]

closed = False
while not closed:
    bytes = client.recv(1024)
    closed = (len(bytes) == 0)
    str = bytes.decode("utf-8")
    print(str)
print("done")