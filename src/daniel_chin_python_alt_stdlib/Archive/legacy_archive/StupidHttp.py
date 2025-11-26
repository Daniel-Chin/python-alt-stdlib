import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 80))
s.listen(1)
(c, address) = s.accept()
c.send('<html><body>Hello? </body></html>'.encode())
input('end')
