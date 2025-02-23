import socket

# create socket object
s = socket.socket()
# define port
port = 12345
# connect to server
s.connect(("127.0.0.1", port))
# print the receive data from server
print(s.recv(1024).decode())
# close the connection
s.close()
