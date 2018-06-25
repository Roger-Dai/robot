# This program defines key functions that can be called to instruct the robot

import math
import socket
import time
import sys

HOST = '140.233.20.115'
PORT = 30000
# PORT2 = 30001
PORT2 = 30002

ORIGINAL = "movel(p[0.253382,-0.0770761,0.410262,-1.99486,-0.096691,-1.87748], a = 0.5, v = 0.5)\n"
# SECOND1 = "movel(p[0.267397,-0.0790473,0.409577,-2.03338,-0.0205629,-1.92116], a = 0.5, v = 0.5)\n"
# SECOND2 = "movel(p[0.435683,0.0268291,0.425731,-2.18414,0.0709854,-2.04954], a = 0.5, v = 0.5)\n"
NEXT = "movel(p[0.455506,-0.0263883,0.405709,-2.08937,0.139225,-2.01385], a = 0.5, v = 0.5)\n"
DOWN = "def Move():\nmovel(p[0.253388,-0.0770718,0.410261,-1.99481,-0.0967188,-1.8774], a = 50, v = 25)\nend\n"
UP = "def Move():\nmovel(p[0.270365,-0.100752,0.789496,1.70422,1.01859,2.15213], a = 50, v = 25)\nend\n"
LOW = "def Move():\nmovej(p[0.246217,0.0843333,0.360932,-1.32081,-1.50092,-2.13922], a = 10, v = 10)\nend\n"
HIGH = "def Move():\nmovej(p[0.150559,-0.377884,0.800775,0.819544,1.30144,0.823734], a = 10, v = 10)\nend\n"

POSE = "def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,0.2032,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.5, v = 0.5)\nend\n"



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
    s = client_socket()
    s.send(ORIGINAL.encode("utf-8"))


def next_position():
    s = client_socket()
    s.send(NEXT.encode("utf-8"))


def up(a, v):
    s = client_socket()

    temp = UP
    index1 = temp.find("a = ")
    index2 = temp.find(", v = ")
    temp = temp[ : (index1 + 4)] + str(a) + temp[index2 :]
    index1 = temp.find("v = ")
    index2 = temp.find(")", index1)
    temp = temp[ : (index1 + 4)] + str(v) + temp[index2 :]
    
    s.send(temp.encode("utf-8"))


def down(a, v):
    s = client_socket()

    temp = DOWN
    index1 = temp.find("a = ")
    index2 = temp.find(", v = ")
    temp = temp[ : (index1 + 4)] + str(a) + temp[index2 :]
    index1 = temp.find("v = ")
    index2 = temp.find(")", index1)
    temp = temp[ : (index1 + 4)] + str(v) + temp[index2 :]

    s.send(temp.encode("utf-8"))


def low(a, v):
    s = client_socket()

    temp = LOW
    index1 = temp.find("a = ")
    index2 = temp.find(", v = ")
    temp = temp[ : (index1 + 4)] + str(a) + temp[index2 :]
    index1 = temp.find("v = ")
    index2 = temp.find(")", index1)
    temp = temp[ : (index1 + 4)] + str(v) + temp[index2 :]

    s.send(temp.encode("utf-8"))


def high(a, v):
    s = client_socket()

    temp = HIGH
    index1 = temp.find("a = ")
    index2 = temp.find(", v = ")
    temp = temp[ : (index1 + 4)] + str(a) + temp[index2 :]
    index1 = temp.find("v = ")
    index2 = temp.find(")", index1)
    temp = temp[ : (index1 + 4)] + str(v) + temp[index2 :]

    s.send(temp.encode("utf-8"))


def move_pose(pose, a, v):
    s = client_socket()

    temp = "def Move():\nmovel(p[" + pose + "], a = 1, v = 1)\nend\n"
    index1 = temp.find("a = ")
    index2 = temp.find(", v = ")
    temp = temp[ : (index1 + 4)] + str(a) + temp[index2 :]
    index1 = temp.find("v = ")
    index2 = temp.find(")", index1)
    temp = temp[ : (index1 + 4)] + str(v) + temp[index2 :]
    print(temp)

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
    print(temp)

    s.send(temp.encode("utf-8"))


def powerdown():
    s = client_socket()
    s.send("powerdown()\n".encode("utf-8"))


def linearX(d, a, v):
    s = client_socket()

    temp = "def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0," + d + ",0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovej(Target, a = 0.5, v = 0.5)\nend\n"
    index1 = temp.find("a = ")
    index2 = temp.find(", v = ")
    temp = temp[ : (index1 + 4)] + str(a) + temp[index2 :]
    index1 = temp.find("v = ")
    index2 = temp.find(")", index1)
    temp = temp[ : (index1 + 4)] + str(v) + temp[index2 :]

    s.send(temp.encode("utf-8"))


def linearY(d, a, v):
    s = client_socket()

    temp = "def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0," + d + ",0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovej(Target, a = 0.5, v = 0.5)\nend\n"
    index1 = temp.find("a = ")
    index2 = temp.find(", v = ")
    temp = temp[ : (index1 + 4)] + str(a) + temp[index2 :]
    index1 = temp.find("v = ")
    index2 = temp.find(")", index1)
    temp = temp[ : (index1 + 4)] + str(v) + temp[index2 :]

    s.send(temp.encode("utf-8"))

def linearZ(d, a, v):
    s = client_socket()

    temp = "def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[" + d + ",0.0,0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovej(Target, a = 0.5, v = 0.5)\nend\n"
    index1 = temp.find("a = ")
    index2 = temp.find(", v = ")
    temp = temp[ : (index1 + 4)] + str(a) + temp[index2 :]
    index1 = temp.find("v = ")
    index2 = temp.find(")", index1)
    temp = temp[ : (index1 + 4)] + str(v) + temp[index2 :]

    s.send(temp.encode("utf-8"))


def toggle():
    s = client_socket()
    if counter % 2 == 0:
        s.send(NEXT.encode("utf-8"))
        print("Moved the robot to the left. The robot will move to the right next.")
    else:
        s.send(ORIGINAL.encode("utf-8"))
        print("Moved the robot to the right. The robot will move to the left next.")

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


# -------------------------------------------------------- FOR FUN -------------------------------------------------------------
#START = "movej(p[0.240286,-0.058284,0.41337,-1.85913,-0.605021,-1.90478], a = 0.5, v = 0.5)\n"
START = "movej(p[0.122562,-0.163207,0.438395,-1.91079,-0.626631,-1.86714], a = 0.5, v = 0.5)\n"
# START = "movej(p[0.642519,-0.313894,0.277338,0.148518,-1.54961,-0.163963], a = 0.5, v = 0.5)\n"
# SQUARE = 'def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,0.4,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5, r = 0.1)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.4,0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5, r = 0.1)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,-0.4,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5, r = 0.1)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,-0.4,0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5, r = 0.1)\nend\n'
SQUARE = 'def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,0.4,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.4,0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,-0.4,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,-0.4,0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nend\n'
# SQUARE = 'def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,0.4,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nsleep(1)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.4,0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nsleep(1)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,-0.4,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nsleep(1)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,-0.4,0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nend\n'
STAR = "def Star():\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[-0.36,-0.12,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[0.24,0.28,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[0,-0.32,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[-0.24,0.28,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[0.36,-0.12,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nend\n"
ARC = "def Arc():\nCurPos = get_actual_tcp_pose()\nTarget = pose_trans(CurPos, p[0,0,0.001,0,0,0])\nVia = pose_trans(CurPos, p[0,0.2,0.2,0,0,0])\nmovec(Via, Target, a = 0.1, v = 0.1)\nend\n"
CURVE = "def SmoothSquare():\nCurPos≔get_forward_kin()\nheight≔100\nwidth≔100\nblend_radius≔50\nwhile (True):\ncorner_1=pose_trans(CurPos,p[width/1000.0,0.0,0.0,0.0,0.0,0.0])\nmovel(corner_1,1.2,0.25,blend_radius/1000.0)\ncorner_2=pose_trans(CurPos,p[width/1000.0,height/1000.0,0.0,0.0,0.0,0.0])\nmovel(corner_2,1.2,0.25,blend_radius/1000.0)\ncorner_3=pose_trans(CurPos,p[0.0,height/1000.0,0.0,0.0,0.0,0.0])\nmovel(corner_3,1.2,0.25,blend_radius/1000.0)\nmovel(CurPos,1.2,0.25,blend_radius/1000.0)\nend\nend\n"


def start():
    s = client_socket()
    s.send(START.encode("utf-8"))


def square():
    s = client_socket()
    s.send(SQUARE.encode("utf-8"))
    

def star():
    s = client_socket()
    s.send(STAR.encode("utf-8"))


def arc():
    s = client_socket()
    s.send(ARC.encode("utf-8"))


def square1(back):
    s = client_socket()
    if back == 0:    
        temp = "def line():\nCurPos = get_actual_tcp_pose()\nTarget = pose_trans(CurPos, p[0,0,0.4,0,0,0])\nmovel(Target, a = 0.3, v = 0.3)\nend\n"
    elif back == 1:
        temp = "def line():\nCurPos = get_actual_tcp_pose()\nTarget = pose_trans(CurPos, p[0,0,-0.4,0,0,0])\nmovel(Target, a = 0.3, v = 0.3)\nend\n"
    
    s.send(temp.encode("utf-8"))


def square2(back):
    s = client_socket()
    if back == 0:    
        temp = "def line():\nCurPos = get_actual_tcp_pose()\nTarget = pose_trans(CurPos, p[0,0.4,0,0,0,0])\nmovel(Target, a = 0.3, v = 0.3)\nend\n"
    elif back == 1:
        temp = "def line():\nCurPos = get_actual_tcp_pose()\nTarget = pose_trans(CurPos, p[0,-0.4,0,0,0,0])\nmovel(Target, a = 0.3, v = 0.3)\nend\n"

    s.send(temp.encode("utf-8"))


def square3(back):
    s = client_socket()
    if back == 0:
        temp = "def line():\nCurPos = get_actual_tcp_pose()\nTarget = pose_trans(CurPos, p[0,0,-0.4,0,0,0])\nmovel(Target, a = 0.3, v = 0.3)\nend\n"
    elif back == 1:
        temp = "def line():\nCurPos = get_actual_tcp_pose()\nTarget = pose_trans(CurPos, p[0,0,0.4,0,0,0])\nmovel(Target, a = 0.3, v = 0.3)\nend\n"
    s.send(temp.encode("utf-8"))


def square4(back):
    s = client_socket()
    if back == 0:
        temp = "def line():\nCurPos = get_actual_tcp_pose()\nTarget = pose_trans(CurPos, p[0,-0.4,0,0,0,0])\nmovel(Target, a = 0.3, v = 0.3)\nend\n"
    elif back == 1:
        temp = "def line():\nCurPos = get_actual_tcp_pose()\nTarget = pose_trans(CurPos, p[0,0.4,0,0,0,0])\nmovel(Target, a = 0.3, v = 0.3)\nend\n"    
    s.send(temp.encode("utf-8"))


def curve():
    s = client_socket()
    s.send(CURVE.encode("utf-8"))
    



    
# -------------------------------------------------------- FOR FUN -------------------------------------------------------------


def arm():
    # ARM = "def arm():\nmovej(p[0.638731,-0.379671,0.138594,0.230583,-1.59305,-0.0423721], a = 0.5, v = 0.5, t = 3)\nmovej(p[0.522702,-0.376583,0.155042,0.407091,-1.49957,0.0952902], a = 0.5, v = 0.5, t = 3)\nmovej(p[0.413804,-0.437115,0.144112,0.553805,-1.46122,0.239321], a = 0.5, v = 0.5, t = 3)\nmovej(p[0.237503,-0.543883,0.143131,0.813332,-1.36816,0.454261], a = 0.5, v = 0.5, t = 3)\nmovej(p[0.105378,-0.626008,0.132268,0.974303,-1.29439,0.684523], a = 0.5, v = 0.5, t = 3)\nend\n"
    # ARM = "def arm():\nmovej(p[0.510353,-0.280654,0.32547,0.272994,-1.53764,-0.0369382], a = 0.5, v = 0.5, t = 3, r = 0.05)\nmovej(p[0.383958,-0.344475,0.335196,0.488167,-1.50189,0.196437], a = 0.5, v = 0.5, t = 3, r = 0.05)\nmovej(p[0.151416,-0.493351,0.292381,0.81161,-1.37066,0.558083], a = 0.5, v = 0.5, t = 4, r = 0.05)\nmovej(p[0.0317325,-0.60131,0.301975,0.955632,-1.27667,0.736863], a = 0.5, v = 0.5, t = 3, r = 0.05)\nend\n"
    ARM = "def arm():\nmovej(p[0.510353,-0.280654,0.32547,0.272994,-1.53764,-0.0369382], a = 0.5, v = 0.5, t = 2)\nsleep(3)\nmovej(p[0.383958,-0.344475,0.335196,0.488167,-1.50189,0.196437], a = 0.5, v = 0.5, t = 2)\nsleep(3)\nmovej(p[0.151416,-0.493351,0.292381,0.81161,-1.37066,0.558083], a = 0.5, v = 0.5, t = 3)\nsleep(3)\nmovej(p[0.0317325,-0.60131,0.301975,0.955632,-1.27667,0.736863], a = 0.5, v = 0.5, t = 2)\nend\n"
    # ARM = "def arm():\nmovej(p[0.510353,-0.280654,0.32547,0.272994,-1.53764,-0.0369382], a = 0.5, v = 0.5, t = 2)\nsleep(0.5)\nmovej(p[0.383958,-0.344475,0.335196,0.488167,-1.50189,0.196437], a = 0.5, v = 0.5, t = 2)\nsleep(0.5)\nmovej(p[0.151416,-0.493351,0.292381,0.81161,-1.37066,0.558083], a = 0.5, v = 0.5, t = 3)\nsleep(0.5)\nmovej(p[0.0317325,-0.60131,0.301975,0.955632,-1.27667,0.736863], a = 0.5, v = 0.5, t = 2)\nend\n"
    # ARM = "def arm():\nmovej(p[0.510353,-0.280654,0.32547,0.272994,-1.53764,-0.0369382], a = 0.5, v = 0.5, t = 2, r = 0.05)\nmovej(p[0.383958,-0.344475,0.335196,0.488167,-1.50189,0.196437], a = 0.5, v = 0.5, t = 2, r = 0.05)\nmovej(p[0.151416,-0.493351,0.292381,0.81161,-1.37066,0.558083], a = 0.5, v = 0.5, t = 3, r = 0.05)\nmovej(p[0.0317325,-0.60131,0.301975,0.955632,-1.27667,0.736863], a = 0.5, v = 0.5, t = 2, r = 0.05)\nend\n"
    
    s = client_socket()
    s.send(ARM.encode("utf-8"))


if __name__ == "__main__":
    counter = 0
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
            print("freedrive")
        if x == "end freedrive":
            end_freedrive()
            print("end")
        if x == "powerdown":
            powerdown()
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
            counter = counter + 1
        if x == "next":
            next_position()
            counter = counter + 1
        if x == "toggle":
            toggle()
            counter = counter + 1
        if x == "up":
            y = input("Enter a and v: ")
            y = y.split(" ")
            a = float(y[0])
            v = float(y[1])
            up(a, v)
        if x == "down":
            y = input("Enter a and v: ")
            y = y.split(" ")
            a = float(y[0])
            v = float(y[1])
            down(a, v)
        if x == "low":
            y = input("Enter a and v: ")
            y = y.split(" ")
            a = float(y[0])
            v = float(y[1])
            low(a, v)
        if x == "high":
            y = input("Enter a and v: ")
            y = y.split(" ")
            a = float(y[0])
            v = float(y[1])
            high(a, v)
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
        if x == "square":
            square()
        if x == "star":
            star()
        if x == "arc":
            arc()
        if x == "start":
            start()
        if x == "1":
            y = int(input("Backward? "))
            square1(y)
        if x == "2":
            y = int(input("Backward? "))
            square2(y)
        if x == "3":
            y = int(input("Backward? "))
            square3(y)
        if x == "4":
            y = int(input("Backward? "))
            square4(y)
        if x == "curve":
            curve()
        if x == "arm":
            arm()
