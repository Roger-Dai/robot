import socket
import time

HOST = "140.233.20.115"
# HOST = "140.233.173.238"
PORT = 30000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", PORT)) # Bind to the port 
s.listen(5) # Now wait for client connection.
(clientsocket, addr) = s.accept() # Establish connection with client.
print("Accepted socket connection.")
while True:
    input()
    clientsocket.send("go".encode())

byte = clientsocket.send(bytes(1))
print(byte)
