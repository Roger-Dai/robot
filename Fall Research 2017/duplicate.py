import socket
import time

HOST = "140.233.20.115"
# HOST = "140.233.173.238"
PORT = 30001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send("movej([-1.18, -1.58, 1.16, -1.15, -1.55, 1.18], a=1.0, v=0.1)\n")
time.sleep(2)
s.send("movej([-1.95, -1.58, 1.16, -1.15, -1.55, 1.18], a=1.0, v=0.1)\n")
time.sleep(2)
s.send("movej([-1.27, -1.58, 1.16, -1.15, -1.55, 1.18], a=1.0, v=0.1)\n")
time.sleep(2)
