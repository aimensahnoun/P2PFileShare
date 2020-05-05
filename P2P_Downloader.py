import socket
import json
import os
from datetime import datetime

# content_name is same as in server file now
extension = ''


def checkLeng(*args):
    files = os.listdir(path)
    length = 0
    for q in chunkNames:
        if q in files:
            length += 1
    return length


def deleteUselessFiles(*args):
    files = os.listdir(path)
    for q in chunkNames:
        if q in files:
            os.remove(path + '/' + q)


while True:

    if 'P2PDownloadFolder' in os.listdir(os.curdir):
        path = os.getcwd() + '/P2PDownloadFolder'
    else:
        path = os.getcwd() + '/P2PDownloadFolder'
        os.mkdir(path)

    log = open("DownloadLog.txt", 'a')
    filename = input("Please enter the file name you want to download: ")

    port = 5001

    # again, this'll be the name of the conten
    # t that used wanted to download from the network.
    chunkNames = [filename + '_1', filename + '_2', filename + '_3', filename + '_4', filename + '_5']

    file = open("contentDictionary.txt", "r")
    nameCheck = True
    contentDictionary = json.loads(file.read())

    file.close()
    for file in chunkNames:
        if file not in contentDictionary.keys():
            nameCheck = False
    while not nameCheck:
        filename = input(filename + ' is not being hosted by anyone, please try again : ')
        chunkNames = [filename + '_1', filename + '_2', filename + '_3', filename + '_4', filename + '_5']
        for file in chunkNames:
            if file in contentDictionary.keys():
                nameCheck = True
    while True:
        for chunk in chunkNames:
            ips = contentDictionary[chunk]
            ips = ips.split(',')
            tries = 0
            for ip in ips:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(5)
                    s.connect((ip, port))

                    message = {'filename': chunk}
                    message = json.dumps(message).encode('utf-8')
                    s.send(bytes(message))

                    with open(path + '/' + chunk, 'wb') as f:

                        while True:
                            print('receiving data...')
                            data = s.recv(9999999)

                            if not data:
                                break
                            # write data to a file
                            f.write(data)

                    f.close()
                    time = datetime.now()
                    logmessage = str(time) + ' , ' + chunk + ' , ' + 'downloaded from : ' + ip + '\n'
                    print(logmessage)
                    log.write(logmessage)
                    s.send(bytes('download done', 'utf-8'))

                except socket.error:
                    print('Connection timed out with : ' + ip)
                    tries += 1
                finally:
                    s.close()
            if tries == len(ips):
                print("CHUNK " + chunk + " CANNOT BE DOWNLOADED FROM ONLINE PEERS")
        log.close()
        break

    # with open(content_name+'.png', 'w') as outfile:
    length = checkLeng(chunkNames)
    if length == 5:
        extension = input('please enter the extension of original file: ')
        newPath = path + '/' + filename + extension
        print(newPath)
        with open(newPath,
                  'w+b') as outfile:  # in your code change 'ece.png' to content_name+'.png'
            for chunk in chunkNames:
                print(chunk)
                with open(path + '/' + chunk, 'rb') as infile:
                    outfile.write(infile.read())
        print("File successfully downloaded!")
    elif length == 0:
        print('Failed to download file!\nPlease try again some other time')
    else:
        print("Some files are missing, cannot repack the original file")
        opinion = input("Do you want to delete the corrupted files ? Y/N :")
        if opinion.lower() == 'y':
            deleteUselessFiles(chunkNames)
    resume = input("Do you want to download another file ? Y/N: ")
    if resume.lower() != 'y':
        break
