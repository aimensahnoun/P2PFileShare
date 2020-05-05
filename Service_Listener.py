import socket
import json

receiver = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
ip = socket.gethostbyname(socket.gethostname())


receiver.bind(('', 5000))

contentDictionary = {}


def contentManager(*args):
    for file in files:
        if file in contentDictionary.keys():
            if user_ip in contentDictionary[file]:
                break
            else:
                contentDictionary[file] = contentDictionary[file] + ',' + user_ip
        else:
            contentDictionary.update({file: user_ip})


while True:
    data, address = receiver.recvfrom(1024)  # buffer size is 1024 bytes
    receivedMessage = json.loads(data)
    username = receivedMessage["username"]
    user_ip = address[0]
    files = receivedMessage["files"]
    print(username + " : " + str(files))
    contentManager(files, user_ip)
    file = open("contentDictionary.txt", "w")
    file.write(json.dumps(contentDictionary))
    file.close()
