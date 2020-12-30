#!/usr/bin/python
import os
from time import sleep
import socket
import signal
import config
connected = False
username = os.environ.get("USER")



def handler(signum, frame):
    if connected == True:
        global username
        send_message("User_left:{}".format(username))
        quit()

def send_message(msg):
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.settimeout(60.0)
            addr = ("127.0.0.1",8080)
            client_socket.bind(('', 8081))
            client_socket.sendto(msg.encode("utf-8"), addr)
            message, address = client_socket.recvfrom(1024)
            print(message)
            client_socket.close()
            return message
        except Exception as e:
            print("Error: {}".format(e))
            sleep(1)


with open(config.MOTD_PATH,"r") as f:
    for l in f:
        print(l[:-1])

send_message("Connect:{}".format(username))
connected = True

signal.signal(signal.SIGHUP,handler)
signal.signal(signal.SIGTSTP,handler)
try:
    while True:
        command = raw_input(":")
        if command.lower() == "disconnect":
            if connected == True:
                send_message("Disconnect:{}".format(username))
                quit()
except KeyboardInterrupt:
    handler(1,1)
