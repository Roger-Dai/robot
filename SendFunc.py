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

# motion =  "def move():\nmovej(p[0.34836,-0.16461,0.11501,1.5447,0.97633,-2.8218], a = 0.3, v = 0.3, r = 0.01)\nend\n"
motion = "movej(p[-0.21213,-0.40218,0.28873,3.04,-1.4736,2.6895], a = 0.1, v = 0.1, r = 0.01)\n"

ORIGINAL = "movel(p[0.253382,-0.0770761,0.410262,-1.99486,-0.096691,-1.87748], a = 0.3, v = 0.3)\n"

TRAJ = "def move():\nmovej([1.939595, -1.137267, 1.892716, -2.222549, 1.498647, -1.725285],a = 0.3, v = 0.3)\nmovej([1.577594, -1.263043, 2.055875, -2.265782, 1.508959, -1.089949],a = 0.3, v = 0.3)\nmovej([1.290230, -1.159774, 1.847007, -2.187856, 1.527386, -0.360883],a = 0.3, v = 0.3)\nmovej([1.654617, -1.261376, 1.980366, -2.266704, 1.524052, -1.157876],a = 0.3, v = 0.3)\nmovej([2.184156, -0.566577, 0.793269, -1.649595, 1.426592, -2.923625],a = 0.3, v = 0.3)\nmovej([1.992565, -1.134733, 1.814173, -2.124117, 1.450125, -2.081070],a = 0.3, v = 0.3)\nmovej([1.844153, -1.216466, 2.041191, -2.291465, 1.409191, -1.695022],a = 0.3, v = 0.3)\nend\n"
# TRAJ = "def move():\nmovej([1.939595, -1.137267, 1.892716, -2.222549, 1.498647, -1.725285],a = 0.3,v = 0.3)\nend\n"

MOVE = "def move():\nmovej(p[0.482794,-0.369096,0.210963,0.273296,0.510005,-2.42687], a = 0.3, v = 0.3)\nmovej(p[0.355939,-0.376458,0.26598,0.307452,0.489899,-2.18725], a = 0.3, v = 0.3)\nmovej(p[0.268856,-0.421868,0.250672,0.163048,0.525763,-1.99444], a = 0.3, v = 0.3)\nmovej(p[0.16055,-0.484803,0.252628,0.0741555,0.451003,-1.74087], a = 0.3, v = 0.3)\nmovej(p[0.068226,-0.585313,0.258928,-0.0215307,0.455378,-1.45914], a = 0.3, v = 0.3)\nend\n"

FIRST = "movej(p[0.190058,-0.38373,0.175607,-0.0212344,0.432451,-1.80717], a = 0.3, v = 0.3)\n"

# SCENE = "def move():\nmovej(p[-0.132367,-0.762148,0.231557,-0.0972441,0.205084,-1.06393], a = 0.3, v = 0.3)\nmovej(p[-0.0324978,-0.462038,0.231683,-0.142894,0.189382,-1.46627], a = 0.3, v = 0.3)\nmovej(p[0.16752,-0.362036,0.231711,0.0770738,0.317893,-1.84835], a = 0.3, v = 0.3)\nmovej(p[0.417497,-0.271971,0.231746,-0.0161138,0.364208,-2.40773], a = 0.3, v = 0.3)\nmovej(p[0.617501,-0.271981,0.231704,-0.0908885,0.388979,-2.77308], a = 0.3, v = 0.3)\nend\n"
SCENE = "def move():\nmovej(p[0.16752,-0.362036,0.231711,0.0770738,0.317893,-1.84835], a = 0.3, v = 0.3)\nend\n"

ANIMALS = "def move():\nmovej(p[-0.0948469,-0.764105,0.182308,-0.0865267,0.305646,-1.14355], a = 0.3, v = 0.3)\nmovej(p[0.0327354,-0.559574,0.170428,-0.0235174,0.37689,-1.54315], a = 0.3, v = 0.3)\nmovej(p[0.190058,-0.38373,0.175607,-0.0212344,0.432451,-1.80717], a = 0.3, v = 0.3)\nmovej(p[0.360815,-0.269423,0.169429,0.0845107,0.40807,-2.16599], a = 0.3, v = 0.3)\nmovej(p[0.564781,-0.241304,0.171022,0.116417,0.360269,-2.45988], a = 0.3, v = 0.3)\nend\n"

s.send(FIRST.encode("utf-8"))
