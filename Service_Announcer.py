import socket
import time
import os
import json

username = input("Please input your username: ")
ip = socket.gethostbyname(socket.gethostname())

IP = ip.split('.')
IP[3] = '255'
ip = '.'.join(IP)

files = []


def getFiles(*args):
    for file in os.listdir(os.curdir):
        if '.' not in file:
            files.append(file)


getFiles(files)

t = {'username': username, 'files': files}

message = json.dumps(t)

service = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP);

service.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    service.sendto(bytes(message, "utf-8"), (ip, 5000))
    print("message sent!")
    time.sleep(60)
