import socket

HOST = '10.209.1.45'    # The remote host
PORT = 2333             # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
for i in range(3):
    data = s.recv(1024)
    print(data.decode())
s.close()
