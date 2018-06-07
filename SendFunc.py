import socket

HOST = '140.233.20.115'
PORT = 30001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

func1 = "def Move():\nset_digital_out(1,True)\nmovej([-1.353230615918169, -0.9105038005127148, -2.363083898161912, 0.195608666035183, 0.6008930202640654, 0.708749062236389], a=1, v=1)\nset_digital_out(1,False)\nend\n"
NEXT = "def Move():\nset_digital_out(1,True)\nmovej([2.107288888888889, -2.0619333333333336, 1.953428888888889, -6.09665888888889, 0.27998333333333336, -4.548638888888889], a=1, v=1)\nset_digital_out(1,False)\nend\n"

s.send(NEXT.encode("utf-8"))
