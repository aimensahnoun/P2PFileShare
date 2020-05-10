import socket
import time
import os
import json

username = input("Please input your username: ")
ip = socket.gethostbyname(socket.gethostname())

IP = ip.split('.')
IP[3] = '255'
ip = '.'.join(IP)




def getFiles(*args):
    for file in os.listdir(os.curdir):
        if os.path.isdir(os.path.join(os.curdir, file)):
            for subFile in os.listdir(os.path.join(os.curdir, file)):
                if '.' not in subFile and subFile not in files:
                    files.append(subFile)
        if '.' not in file and file not in files:
            files.append(file)


service = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP);

service.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    files = []
    getFiles(files)
    t = {'username': username, 'files': files}
    message = json.dumps(t)
    service.sendto(bytes(message, "utf-8"), (socket.gethostbyname(socket.gethostbyname()), 5000))
    print("message sent!")
    time.sleep(60)
