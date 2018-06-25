import socket

HOST = '140.233.20.115'
PORT = 30001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

func1 = "def Move():\nset_digital_out(1,True)\nmovej([-1.353230615918169, -0.9105038005127148, -2.363083898161912, 0.195608666035183, 0.6008930202640654, 0.708749062236389], a=1, v=1)\nset_digital_out(1,False)\nend\n"
NEXT = "def Move():\nset_digital_out(1,True)\nmovej([2.107288888888889, -2.0619333333333336, 1.953428888888889, -6.09665888888889, 0.27998333333333336, -4.548638888888889], a=1, v=1)\nset_digital_out(1,False)\nend\n"

Displacement = "def Move():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0,0,-0.5,0,0,0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.3, v = 0.5)\nend\n"

POSE = "def Pose():\nCurPos = get_actual_tcp_pose()\nDisplacement = p[0.0,0.0,0.2032,0.0,0.0,0.0]\nTarget = pose_trans(CurPos, Displacement)\nmovel(Target, a = 0.5, v = 0.5)\nend\n"
ARC = "def Arc():\nCurPos = get_actual_tcp_pose()\nTarget = pose_trans(CurPos, p[0,0,0.001,0,0,0])\nVia = pose_trans(CurPos, p[0,0.15,0.15,0,0,0])\nmovec(Via, Target, a = 0.1, v = 0.1)\nend\n"

star = "def Star():\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[-0.36,-0.12,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[0.24,0.28,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[0,-0.32,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[-0.24,0.28,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nCurPos = get_forward_kin()\nTarget = pose_trans(CurPos, p[0.36,-0.12,0,0,0,0])\nmovel(Target, a = 0.3, v = 1)\nend\n"


s.send(ARC.encode("utf-8"))
