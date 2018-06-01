import socket
import ctypes

UR5_HOST = "140.233.20.115"
UR5_PORT = 30002

class UR5:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    class Pose:
        #[x, y, z, ax, ay, az]
        #given in axis-angle notation
        orientation = (0, 0, 0, 0, 0, 0)
        
        def __init__(self, x, y, z, ax, ay, az):
            self.orientation = (x,y,z,ax,ay,az)
            return

        def AxisAngle(self):
            return self.orientation
    
    def Connect(self):
        self.sock.connect((UR5_HOST, UR5_PORT))
        
        #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #sock.bind(("", 30002))
        return

    def MoveL(self, pose, a=1, v=1):
        self.sock.send("movel(p[{0},{1},{2},{3},{4},{5}],a={6},v={7})\n".
                  format(*pose.AxisAngle(), a, v).encode()
                       )
        return



    class Packet:        
        packet_length = ctypes.c_int()
        message_type = ctypes.c_uint8()

        class Package:
            ROBOT_MODE_DATA = 0
            JOINT_DATA = 1
            TOOL_DATA = 2
            MASTERBOARD_DATA = 3
            CARTESIAN_INFO = 4
            KINEMATICS_INFO = 5
            CONFIGURATION_DATA = 6
            FORCE_MODE_DATA = 7
            ADDITIONAL_INFO = 8
            CALIBRATION_DATA = 9
            SAFETY_DATA = 10
            
            package_length = ctypes.c_uint()
            package_type = ctypes.c_uint8()
            
            def Recv(self, sock):
                self.package_length = ctypes.c_int(sock.recv(4))
                self.package_type = ctypes.c_uint8(sock.recv(1))
                print('Package type: ', self.package_type)
                return

        def Recv(self, sock):
            buffer = ctypes.create_string_buffer(4) # receive packet length
            buffer.raw = sock.recv(4)
            self.packet_length = ctypes.c_uint.from_buffer_copy(buffer)
            buffer = ctypes.create_string_buffer(1) # receive message type
            buffer.raw = sock.recv(1)
            self.message_type = ctypes.c_uint8.from_buffer_copy(buffer)
            print('Length of package: ', self.packet_length)
            print('Message type: ', self.message_type)
            

