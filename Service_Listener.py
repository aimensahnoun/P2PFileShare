import socket
import json

receiver = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
ip = socket.gethostbyname(socket.gethostname())


receiver.bind(('', 5000))

contentDictionary = {}


def contentManager(inputfiles,givenip):
    for n in inputfiles:
        if n in contentDictionary.keys():
            if givenip not in contentDictionary[n]:
                contentDictionary[n].append(givenip)
        else:
            ips = [givenip] 
            contentDictionary.update({n: ips})
   
    

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
    
