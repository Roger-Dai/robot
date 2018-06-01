import socket
import time
import re

scriptp = './test.urscript'
host = "140.233.20.115"
port = 30002

aux_fn_dict = {
        'sleep\((\d+)\)' : 'time.sleep({0})'
    }

def compile_regex(regex2fmt):
    return dict(map(lambda pair: (re.compile(pair[0]), pair[1]), aux_fn_dict.items()))

aux_fn_dict = compile_regex(aux_fn_dict)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

status_channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
with open(scriptp, 'r') as scriptf:
    for line in scriptf:
        for (pattern, fmt) in aux_fn_dict.items():
            match = pattern.match(line)
            if match:
                aux_fn = fmt.format(*match.groups())
                print(aux_fn)
                eval(aux_fn)
            else:
                s.send(line.encode())


print('Script sent.')
status_channel.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
status_channel.bind(("", 30000)) # Bind to the port 
status_channel.listen(5) # Now wait for client connection.
print('Connection established.')
# status_channel.connect(("", 30000))
status_channel.accept() # Establish connection with client.

print('Sending byte...')
s.send("socket_send_byte(128)\n".encode())

l = status_channel.recv(1)
print('Byte received: ' + l)

