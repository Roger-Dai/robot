# This is the Python file that runs on the comupter to teach the robot different poses.
# This program stores those positions in a list and moves the robot arm to those poses 
# respectively after all poses are taught.


import socket
from time import sleep
import RobotControl

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


positions = []
while True:
    x = input()
    if x == "done":
        break
    else:
        y = x + "\n"        
    client.send(y.encode("utf-8"))
    if x == "next":
        print("run")
        bytes = client.recv(1024)
        print("break")
        str = bytes.decode("utf-8")
        positions.append(str)
    print(positions)


s.close()
client.close()
print(positions)
print("Teach mode finished")

RobotControl.move(positions)
print("Finished!")

