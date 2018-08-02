# This program defines key functions that can be called to instruct the robot

import math
import socket
import time
import sys

HOST = '140.233.20.115'
PORT = 30000
# PORT2 = 30001
PORT2 = 30002

def move(positions):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT2))
    print("Starting Program")
    count = 0
    while (count < 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT2))
        time.sleep(0.5)
        for i in positions:
            temp = "movej(" + i.rstrip() + ", a=1.0, v=0.1)\n"
            s.send(temp.encode("utf-8"))
            time.sleep(10)
        count = count + 1
    print("Program finish")
    time.sleep(1)
    s.close()


def freedrive():
    # client = server()
    client.send("freedrive\n".encode("utf-8")) # pylint: disable=E1101


def end_freedrive():
    # client = server()
    client.send("end_freedrive\n".encode("utf-8")) # pylint: disable=E1101


def return_pose():
    # client = server()
    client.send("return_pose\n".encode("utf-8")) # pylint: disable=E1101
    bytes = client.recv(1024) # pylint: disable=E1101
    str = bytes.decode("utf-8")
    return str


def return_joint_positions():
    # client = server()
    client.send("return_joint_positions\n".encode("utf-8")) # pylint: disable=E1101
    bytes = client.recv(1024) # pylint: disable=E1101
    str = bytes.decode("utf-8")
    joints = str[1:(len(str) - 1)]
    joints = joints.split(",")
    return (rad_to_deg_list(joints), str)


def rad_to_deg_list(rad):
    degrees = []
    for i in rad:
        i = float(i)
        deg = i * (180 / math.pi)
        degrees.append(deg)
    return degrees


def deg_to_rad_list(deg):
    rads = []
    for i in deg:
        i = float(i)
        rad = i * (math.pi / 180)
        rads.append(rad)
    return rads


def move_pose(pose, a, v):
    s = client_socket()

    temp = "def Move():\nmovel(p[" + pose + "], a = 1, v = 1)\nend\n"
    index1 = temp.find("a = ")
    index2 = temp.find(", v = ")
    temp = temp[ : (index1 + 4)] + str(a) + temp[index2 :]
    index1 = temp.find("v = ")
    index2 = temp.find(")", index1)
    temp = temp[ : (index1 + 4)] + str(v) + temp[index2 :]

    s.send(temp.encode("utf-8"))

    
def move_joints(joints, a, v):
    s = client_socket()

    temp = "def Move():\nmovej([" + joints + "], a = 1, v = 1)\nend\n"
    index1 = temp.find("a = ")
    index2 = temp.find(", v = ")
    temp = temp[ : (index1 + 4)] + str(a) + temp[index2 :]
    index1 = temp.find("v = ")
    index2 = temp.find(")", index1)
    temp = temp[ : (index1 + 4)] + str(v) + temp[index2 :]

    s.send(temp.encode("utf-8"))

def powerdown():
    s = client_socket()
    s.send("powerdown()\n".encode("utf-8"))

def linearZ(d, a, v):
    s = client_socket()

    temp = "def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0," + d + ",0.0,0.0,0.0]\nTarget = pose_add(CurPos, Displacement)\nmovej(Target, a = 0.5, v = 0.5)\nend\n"
    index1 = temp.find("a = ")
    index2 = temp.find(", v = ")
    temp = temp[ : (index1 + 4)] + str(a) + temp[index2 :]
    index1 = temp.find("v = ")
    index2 = temp.find(")", index1)
    temp = temp[ : (index1 + 4)] + str(v) + temp[index2 :]

    s.send(temp.encode("utf-8"))


def linearY(d, a, v):
    s = client_socket()

    temp = "def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0," + d + ",0.0,0.0,0.0,0.0]\nTarget = pose_add(CurPos, Displacement)\nmovej(Target, a = 0.5, v = 0.5)\nend\n"
    index1 = temp.find("a = ")
    index2 = temp.find(", v = ")
    temp = temp[ : (index1 + 4)] + str(a) + temp[index2 :]
    index1 = temp.find("v = ")
    index2 = temp.find(")", index1)
    temp = temp[ : (index1 + 4)] + str(v) + temp[index2 :]

    s.send(temp.encode("utf-8"))

def linearX(d, a, v):
    s = client_socket()

    temp = "def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[" + d + ",0.0,0.0,0.0,0.0,0.0]\nTarget = pose_add(CurPos, Displacement)\nmovej(Target, a = 0.5, v = 0.5)\nend\n"
    index1 = temp.find("a = ")
    index2 = temp.find(", v = ")
    temp = temp[ : (index1 + 4)] + str(a) + temp[index2 :]
    index1 = temp.find("v = ")
    index2 = temp.find(")", index1)
    temp = temp[ : (index1 + 4)] + str(v) + temp[index2 :]

    s.send(temp.encode("utf-8"))


def client_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT2))
    return s


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', PORT))

    s.listen(5)
    temp = s.accept()
    client = temp[0]
    return client


if __name__ == "__main__":
    counter = 0
    if len(sys.argv) != 2:
        print("usage: python3 MasterControl.py (c|n)")
    if sys.argv[1] == "c":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', PORT))
        s.listen(5)
        client, client_addr = s.accept()

    while True:
        x = input("Enter: ")
        if x == "done":
            break
        if x == "freedrive":
            freedrive()
        if x == "end freedrive":
            end_freedrive()
        if x == "powerdown":
            powerdown()
        if x == "pose":
            y = return_pose()
            print("pose:")
            print(y)
        if x == "joints":
            y = return_joint_positions()
            print("joints:")
            print(y)
        if x == "move pose":
            y = input("Enter a and v: ")
            y = y.split(" ")
            a = float(y[0])
            v = float(y[1])
            z = input("Enter six numbers specifying a pose: \n")
            move_pose(z, a, v)
        if x == "move joints":
            y = input("Enter a and v: ")
            y = y.split(" ")
            a = float(y[0])
            v = float(y[1])
            z = input("Enter six numbers specifying joint positions: \n")
            move_joints(z, a, v)
        if x == "linear-x":
            y = input("Enter a and v: ")
            y = y.split(" ")
            a = float(y[0])
            v = float(y[1])
            z = input("Enter distance moved in meters: \n")
            linearX(z, a, v)
        if x == "linear-y":
            y = input("Enter a and v: ")
            y = y.split(" ")
            a = float(y[0])
            v = float(y[1])
            z = input("Enter distance moved in meters: \n")
            linearY(z, a, v)
        if x == "linear-z":
            y = input("Enter a and v: ")
            y = y.split(" ")
            a = float(y[0])
            v = float(y[1])
            z = input("Enter distance moved in meters: \n")
            linearZ(z, a, v)
