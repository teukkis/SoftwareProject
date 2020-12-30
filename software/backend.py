import socket
from time import sleep

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 8080))
addr = ("127.0.0.1", 8081)

while True:
    message,address = server_socket.recvfrom(1024)
    message = message.decode("utf-8")
    print(message)
    if "Connect:" in message:
        server_socket.sendto("You have to forward this port in your PUTTY-settings: 8888", addr)
    elif "Disconnect:" in message:
        server_socket.sendto("Disconnected", addr)
    else:
        server_socket.sendto("Something else", addr)