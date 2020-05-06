import os
import math
import socket
import json
from datetime import datetime

userInput = input("Which file do you wish to host ?\n")

content_name = userInput

# This'll be the parameter you provide for this code. The name of the content that the user wants to download.




def getFile(givenname):
    global CHUNK_SIZE
    global filename
    global state
    temp = os.listdir(os.curdir)
    counter = 0
    for n in temp:
        if givenname.lower() in n.lower():
            counter = counter + 1
            print(counter)
    if counter == 1:
        for n in temp:
            if givenname.lower() in n.lower():
                filename = n
                fsize = os.path.getsize(n)
                CHUNK_SIZE = math.ceil(math.ceil(fsize) / 5)
                state = True
    elif counter > 1:
        extension = input(
            "There are multiple files with the name you inputed, what is the extension of the file you need\n")
        newName = givenname + extension
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

index = 1
while not found:
    newinput = input("Please enter the file name again : ")
    filename, CHUNK_SIZE, found = getFile(newinput)
else:
    with open(filename, 'rb') as infile:
        chunk = infile.read(int(CHUNK_SIZE))
        while chunk:
            chunkname = content_name + '_' + str(index)
            # print("chunk name is: " + chunkname + "\n")
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
            file = open(chunk_name, 'rb')
            while True:
                l = file.read(9999999)
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
