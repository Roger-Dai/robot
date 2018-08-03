import math
import socket
import time
import sys

HOST = '140.233.20.115'
PORT = 30002

# -------------------------------HERE ARE SOME OF THE PRE_RECORDED TRAJECTORIES-------------------------

# SQUARE = 'def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,0.4,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5, r = 0.1)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.4,0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5, r = 0.1)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,-0.4,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5, r = 0.1)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,-0.4,0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5, r = 0.1)\nend\n'
SQUARE = 'def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,0.4,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.4,0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,-0.4,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,-0.4,0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nend\n'
# SQUARE = 'def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,0.4,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nsleep(1)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.4,0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nsleep(1)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,-0.4,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nsleep(1)\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,-0.4,0.0,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nend\n'
STAR = "def Star():\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[-0.36,-0.12,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[0.24,0.28,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[0,-0.32,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[-0.24,0.28,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[0.36,-0.12,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nend\n"
ARC = "def Arc():\nCurPos = get_actual_tcp_pose()\nTarget = pose_trans(CurPos, p[0,0,0.001,0,0,0])\nVia = pose_trans(CurPos, p[0,0.2,0.2,0,0,0])\nmovec(Via, Target, a = 0.1, v = 0.1)\nend\n"
CURVE = "def SmoothSquare():\nCurPos≔get_forward_kin()\nheight≔100\nwidth≔100\nblend_radius≔50\nwhile (True):\ncorner_1=pose_trans(CurPos,p[width/1000.0,0.0,0.0,0.0,0.0,0.0])\nmovel(corner_1,1.2,0.25,blend_radius/1000.0)\ncorner_2=pose_trans(CurPos,p[width/1000.0,height/1000.0,0.0,0.0,0.0,0.0])\nmovel(corner_2,1.2,0.25,blend_radius/1000.0)\ncorner_3=pose_trans(CurPos,p[0.0,height/1000.0,0.0,0.0,0.0,0.0])\nmovel(corner_3,1.2,0.25,blend_radius/1000.0)\nmovel(CurPos,1.2,0.25,blend_radius/1000.0)\nend\nend\n"
ARM = "def move():\nmovej(p[-0.0948469,-0.764105,0.182308,-0.0865267,0.305646,-1.14355], a = 0.3, v = 0.3)\nmovej(p[0.0327354,-0.559574,0.170428,-0.0235174,0.37689,-1.54315], a = 0.3, v = 0.3)\nmovej(p[0.190058,-0.38373,0.175607,-0.0212344,0.432451,-1.80717], a = 0.3, v = 0.3)\nmovej(p[0.360815,-0.269423,0.169429,0.0845107,0.40807,-2.16599], a = 0.3, v = 0.3)\nmovej(p[0.564781,-0.241304,0.171022,0.116417,0.360269,-2.45988], a = 0.3, v = 0.3)\nend\n"

# --------------------------------------------------------------------------------------------------------


def powerdown():
    s = client_socket()
    s.send("powerdown()\n".encode("utf-8"))


def client_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s


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


def arm():    
    s = client_socket()
    s.send(ARM.encode("utf-8"))


if __name__ == "__main__":
    counter = 0
    if len(sys.argv) != 1:
        print("usage: python3 PathMovements.py")

    while True:
        x = input("Enter: ")
        if x == "done":
            break
        if x == "powerdown":
            powerdown()
        if x == "square":
            square()
        if x == "star":
            star()
        if x == "arc":
            arc()
        if x == "square1":
            y = int(input("Backward? "))
            square1(y)
        if x == "square2":
            y = int(input("Backward? "))
            square2(y)
        if x == "square3":
            y = int(input("Backward? "))
            square3(y)
        if x == "square4":
            y = int(input("Backward? "))
            square4(y)
        if x == "curve":
            curve()
        if x == "arm":
            arm()
        if x == "help":
            print("""- help: Get a list of all commands and what they do
- done: Terminate all the connections and the program
- powerdown: Shut down the robot arm remotely
- square: Move the robot arm around in a pre-recorded square on the horizontal plane
- star: Move the robot arm around in a pre-recorded star shape on the vertical plane
- arc: Move the robot arm around in a pre-recorded arc
- curve: Move the robot arm around in a pre-recorded square on the horizontal plane continuously with smoothed out edges
- arm: Move the robot arm around in a pre-recorded arc that scans a scene""")