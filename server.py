import socket

# create socket object
s = socket.socket()
# define port
port = 12345
# bind to the port
s.bind(("", port))

# 5 mean number of connection in queue
s.listen(5)

while True:
    # establish connection with client
    c, addr = s.accept()
    # send message
    c.send("test connection".encode())
    # clode the connection
    c.close()
    break
