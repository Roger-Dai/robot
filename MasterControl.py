# This program defines key functions that can be called to instruct the robot

import math
import socket
import time

ORIGINAL = "movel([2.03577, -2.07755, 1.96136, -6.04823, 0.129896, -4.590090000000001], a = 2, v = 2)\n"
NEXT = "movel([2.107288888888889, -2.0619333333333336, 1.953428888888889, -6.09665888888889, 0.27998333333333336, -4.548638888888889], a = 2.0, v = 2.0)\n"
HOST = '140.233.20.115'
PORT = 30000
PORT2 = 30001


def move(positions):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, 30001))
    print("Starting Program")
    count = 0
    while (count < 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, 30001))
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
    client = server()
    client.send("freedrive\n".encode("utf-8")) # pylint: disable=E1101


def end_freedrive():
    client = server()
    client.send("end_freedrive\n".encode("utf-8")) # pylint: disable=E1101


def return_pose():
    client = server()
    client.send("return_pose\n".encode("utf-8")) # pylint: disable=E1101
    bytes = client.recv(1024) # pylint: disable=E1101
    str = bytes.decode("utf-8")
    return str


def return_joint_positions():
    client = server()
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


def teach():
    positions = []
    client = server()
    while True:
        x = input("Enter: ")
        if x == "done":
            break
        else:
            y = x + "\n"        
        client.send(y.encode("utf-8")) # pylint: disable=E1101
        if x == "next":
            print("run")
            bytes = client.recv(1024) # pylint: disable=E1101
            print("break")
            str = bytes.decode("utf-8")
            positions.append(str)
    return positions


def restore_position():
    s = client()
    s.send(ORIGINAL.encode("utf-8"))


def next_position():
    s = client()
    s.send(NEXT.encode("utf-8"))


def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT2))
    return s


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', PORT))

    s.listen(5)
    client = s.accept()[0]
    return client


if __name__ == "__main__":
    while True:
        x = input("Enter: ")
        if x == "done":
            break
        if x == "freedrive":
            freedrive()
            print("freedrive")
        if x == "end freedrive":
            end_freedrive()
            print("end")
        if x == "pose":
            y = return_pose()
            print("pose")
            print(y)
        if x == "joints":
            y = return_joint_positions()
            print("joints")
            print(y)
        if x == "restore":
            restore_position()
        if x == "next":
            next_position()
