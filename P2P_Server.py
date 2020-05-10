import os
import math
import socket
import json
from datetime import datetime

userInput = input("Which file do you wish to host ?\n")

content_name = userInput


# This'll be the parameter you provide for this code. The name of the content that the user wants to download.

def getPath(chunkname):
    fileFound = False
    for file in os.listdir(os.curdir):
        if file == chunkname:
            path = os.curdir +'/'+chunkname
            fileFound = True
            return path
    if not fileFound:
        for file in os.listdir(os.curdir):
            if os.path.isdir(os.path.join(os.curdir, file)):
                for subFile in os.listdir(os.path.join(os.curdir, file)):
                    if subFile == chunkname:
                        fileFound = True
                        path = os.path.join(os.curdir, file) + '/'+chunkname
                        return path
            


def getFile(givenname):
    global CHUNK_SIZE
    global filename
    global state
    temp = os.listdir(os.curdir)
    counter = 0
    for n in temp:
        if givenname.lower() in n.lower():
            counter = counter + 1
    if counter == 1:
        for n in temp:
            if givenname.lower() in n.lower():
                filename = n
                fsize = os.path.getsize(n)
                CHUNK_SIZE = math.ceil(math.ceil(fsize) / 5)
                state = True
    elif counter > 1:
        newName = input(
            "There are multiple files with the name you inputted, please enter the file's full name with extension : ")

        while newName not in temp:
            newName = input("File not found.Please enter the file's full name with extension again  : ")
        for n in temp:
            if newName.lower() in n.lower():
                filename = n
                fsize = os.path.getsize(n)
                CHUNK_SIZE = math.ceil(math.ceil(fsize) / 5)
                state = True

    else:
        state = False
        print('File not found')
        filename = ''
        CHUNK_SIZE = 0

    return filename, CHUNK_SIZE, state


filename, CHUNK_SIZE, found = getFile(content_name)
holder = filename.split('.')
content_name = holder[0]
index = 1
while not found:
    newinput = input("File not found.Please enter the file name again : ")
    holder = filename.split('.')
    content_name = holder[0]
    filename, CHUNK_SIZE, found = getFile(newinput)
else:
    with open(filename, 'rb') as infile:
        chunk = infile.read(int(CHUNK_SIZE))
        while chunk:
            chunkname = content_name + '_' + str(index)
            with open(chunkname, 'wb+') as chunk_file:
                chunk_file.write(chunk)
            index += 1
            chunk = infile.read(int(CHUNK_SIZE))
        chunk_file.close()

    print("Server ready to host your file.")

    port = 5001
    s = socket.socket()

    s.bind((socket.gethostbyname(socket.gethostname()), port))
    s.listen(100)  # socket is listening

    # a forever loop until we interrupt it or
    # an error occurs
    i = 0
    while True:

        # Establish connection with client.
        c, addr = s.accept()
        ip = addr[0]
        print('Got connection from', addr)

        while True:
            log = open("ServerLog.txt", 'a')
            data = c.recv(1024)

            message = json.loads(data)
            chunk_name = message['filename']

            print(ip + ' is requesting: ' + chunk_name)
            requestedpath = getPath(chunk_name)
            file = open(requestedpath, 'rb')
            while True:
                l = file.read(1024)
                if not l:
                    break

                c.send(l)

            file.close()
            time = datetime.now()
            logmessage = str(time) + ' , ' + 'sent to : ' + ip + ' , sent file name : ' + chunk_name + '\n'
            print(logmessage)
            log.write(logmessage)
            log.close()
            c.close()

            break
