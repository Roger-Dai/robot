# This program defines key functions that can be called to instruct the robot

import socket
import time

HOST = '140.233.20.115'
PORT0 = 30000
PORT1 = 30001

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.bind(('', PORT0))

# s.listen(5)
# temp = s.accept()
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client = temp[0]
# client_addr = temp[1]

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', PORT0))

    s.listen(5)
    temp = s.accept()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = temp[0]
    client_addr = temp[1]
    print("done")
    return client

def move(positions):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT1))
    print("Starting Program")
    count = 0
    while (count < 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT1))
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
    print("connection successful")
    # client = connect()
    
    client.send("freedrive".encode("utf-8"))

def end_freedrive():
    client = connect()
    client.send("end_freedrive".encode("utf-8"))

def return_pose():
    client = connect()
    client.send("return_pose".encode("utf-8"))
    bytes = client.recv(1024)
    str = bytes.decode("utf-8")
    return str

def return_joint_positions():
    client = connect()
    client.send("return_joint_positions".encode("utf-8"))
    bytes = client.recv(1024)
    str = bytes.decode("utf-8")
    return str

def teach():
    client = connect()
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
    return positions