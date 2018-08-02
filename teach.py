# This is the Python file that runs on the comupter to teach the robot different poses.
# This program stores those positions in a list and moves the robot arm to those poses 
# respectively after all poses are taught.

import socket
from time import sleep
import RobotCommands

HOST = '140.233.20.115'
PORT = 30000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', PORT))

s.listen(5)
client, client_addr = s.accept()
positions = []

while True:
    x = input("Enter: ")
    if x == "done":
        break
    else:
        y = x + "\n"        
    if x == "next":
        client.send("return_pose\n".encode("utf-8"))
        bytes = client.recv(1024)
        str = bytes.decode("utf-8")
        positions.append(str)
        # client.send("return_joint_positions\n".encode("utf-8"))
        # bytes = client.recv(1024)
        # str = bytes.decode("utf-8")
        # positions.append(str)
    print(positions)


s.close()
client.close()
print(positions)
print("Teach mode finished")


print("Finished!")

