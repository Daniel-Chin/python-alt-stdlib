import socket

HOST = ''                 # Symbolic name meaning the local host
PORT = 2333             # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
for i in range(3):
    conn.send(input().encode())
conn.close()
