import socket
import threading
import time
import sys

#how to use: 
#app = FTP()
#app.run()

class FTP:
    def __init__(self):

        #global here
        self.wifiConnected = False
        self.fileBlockReceived = [False]
        self.fileBlocks = [0]
        self.fileLength = 0

        self.localIPH = "10.1.0.3"
        self.localIP = "10.0.0.3"

        self.remoteIPH = "10.1.0.2"
        self.remoteIP = "10.0.0.2"

        self.sendPort = 5005
        self.recvPort = 5006

        self.initSocket()
        self.initHeartBeat()

    def initSocket(self):
        self.sockS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockS.bind((self.localIP, self.sendPort))

        self.sockSH = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockSH.bind((self.localIPH, self.sendPort))

        self.sockR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockR.bind((self.localIP, self.recvPort))
        self.sockR.settimeout(1)

        self.sockRH = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockRH.bind((self.localIPH, self.recvPort))
        self.sockRH.settimeout(1)

    def initHeartBeat(self):
        self.sendHeartBeatThread = threading.Thread(target=self.sendHeartbeat)
        self.recvHeartBeatThread = threading.Thread(target=self.receiveHeartbeat)
        self.sendHeartBeatThread.start()
        self.recvHeartBeatThread.start()

    def run(self):
        while True:
            fileName, addr = self.sockR.recvfrom(1024) # buffer size is 1024 bytes
            print "requested file: ", self.fileName

            self.fileBlocks = util.getFileChunks(fileName)
            self.fileLength = len(self.fileBlocks)
            self.fileBlockReceived = [False] * self.fileLength
            
            self.sockS.sendto("Ack " + str(self.fileLength), (self.remoteIP, self.receivePort))

            #TODO send file
            print "Sending file"

            for i in range(fileLength):
                while True:
                    self.sockS.sendto(self.fileBlocks[i], (self.remoteIP, self.receivePort)) # Temporary
                
                    # Receive ACK
                    try:
                        data, addr = self.sockR.recvfrom(1024)
                    except socket.timeout:
                        continue
                    if data.startswith("Ack"):
                        ackNum = int(data.split(" ")[1])  # Temporary
                        self.fileBlockReceived[ackNum] = True
                        print "Ack received ", ackNum
                        break
                    else:
                        print(data)
            
            print "Send file completed"
        
    def receiveFileChunks(self, receiver, sender, isHighSpeed):
        while sum(self.fileBlockReceived) < self.fileLength::
            #print "blockCount:", sum(self.fileBlockReceived), " fileLength:", self.fileLength  # Temporary
            try:
                data, addr = receiver.recvfrom(1024)
            except socket.timeout:
                continue
            seqNum = int(data.split(" ")[0])  # Temporary

            # Send ACK
            if isHighSpeed:
                sender.sendto("Ack " + str(seqNum), (self.remoteIPH, self.recvPort))
            else:
                sender.sendto("Ack " + str(seqNum), (self.remoteIP, self.recvPort))

            self.fileBlocks[seqNum] = data.split(" ")[1:]  # Temporary
            self.fileBlockReceived[seqNum] = True


    def sendHeartbeat(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET, UDP
        sock.bind((self.localIP, 5010))

        while True:
            sock.sendto("HeartBeat", (self.remoteIP, 5009))
            time.sleep(4)

    def receiveHeartbeat(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET, UDP
        sock.bind((self.localIP, 5009))
        sock.settimeout(10)

        if self.wifiConnected:
            print("HURAYYYYYYYYYYYYYYYYYYYY")

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if data.startswith("HeartBeat"):
                    # print "HeartBeat Received"
                    wifiConnected = True
                else:
                    print data
            except socket.timeout:
                # print "Receive Heartheat timeout"
                wifiConnected = False


if __name__ == '__main__':

    app = FTP()
    app.run()

