# This is the Python program that imports RobotControl and allows overall intsructions

import RobotControl
import socket
import time

HOST = '140.233.20.115'
PORT0 = 30000
PORT1 = 30001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', PORT0))

s.listen(5)
temp = s.accept()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = temp[0]
client_addr = temp[1]

x = input("Enter: ")
while x != "done":
    if x == "freedrive":
        RobotControl.freedrive()
        print("freedrive")
    if x == "end freedrive":
        RobotControl.end_freedrive()
        print("end")
    if x == "pose":
        y = RobotControl.return_pose()
        print("pose")
        print(y)
    if x == "joints":
        y = RobotControl.return_joint_positions()
        print("joints")
        print(y)
    x = input("Enter: ")