import socket
import threading
import time
import sys
import util

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
        self.recvAckPort = 5007

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
        
        self.sockRAck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockRAck.bind((self.localIP, self.recvAckPort))
        self.sockRAck.settimeout(1)
        
        self.sockRAckH = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockRAckH.bind((self.localIPH, self.recvAckPort))
        self.sockRAckH.settimeout(1)

    def initHeartBeat(self):
        self.sendHeartBeatThread = threading.Thread(target=self.sendHeartbeat)
        self.recvHeartBeatThread = threading.Thread(target=self.receiveHeartbeat)
        self.sendHeartBeatThread.start()
        self.recvHeartBeatThread.start()

    def run(self):
        recvAckThread = threading.Thread(target=self.receiveAcks, args=(self.sockRAck,))
        recvAckThreadH = threading.Thread(target=self.receiveAcks, args=(self.sockRAckH,))
        recvAckThread.start()
        recvAckThreadH.start()

        while True:
            try:
                fileName, addr = self.sockR.recvfrom(1024) # buffer size is 1024 bytes
            except socket.timeout:
                continue
            print "requested file: ", fileName

            self.fileBlocks = util.getFileChunks(fileName)
            self.fileLength = len(self.fileBlocks)
            self.fileBlockReceived = [False] * self.fileLength
            
            self.sockS.sendto("Ack " + str(self.fileLength), (self.remoteIP, self.recvPort))

            print "Sending file"

            #send file with multithread on multiple link

            sendFileThread = threading.Thread(target=self.sendFileChunks, args=())
            sendFileThread.start()
            
            sendFileThreadH = threading.Thread(target=self.sendFileChunksH, args=())
            sendFileThreadH.start()
                        
            sendFileThread.join()
            sendFileThreadH.join()
            
            #for i in range(self.fileLength):
            #    self.sockS.sendto(self.fileBlocks[i], (self.remoteIP, self.recvPort)) # Temporary
                
            print "Send file completed"

    def sendFileChunks(self):
        #Send file through mobile network
        firstIter = True
        while sum(self.fileBlockReceived) < self.fileLength:
            if not firstIter:
                time.sleep(1) # temporary
            firstIter = False
            for i in range(self.fileLength):
                if not self.fileBlockReceived[i]:
                    self.sockS.sendto(self.fileBlocks[i], (self.remoteIP, self.recvPort)) # Temporary
    
    def sendFileChunksH(self):
        #Send file through wifi
        firstIter = True
        while sum(self.fileBlockReceived) < self.fileLength:
            if not firstIter:
                time.sleep(1) # temporary
            firstIter = False
            for i in range(self.fileLength-1, -1, -1): # backward from fileLength-1 to 0
                if not self.fileBlockReceived[i]:
                    while not self.wifiConnected:
                        if sum(self.fileBlockReceived) >= self.fileLength:
                            return
                        time.sleep(2)
                    self.sockSH.sendto(self.fileBlocks[i], (self.remoteIPH, self.recvPort)) # Temporary

    def receiveAcks(self, sock):
        # Receive ACK
        while True:
            try:
                data, addr = sock.recvfrom(1024)
            except socket.timeout:
                continue
            if data.startswith("Ack"):
                ackNum = int(data.split(" ")[1])  # Temporary
                self.fileBlockReceived[ackNum] = True
                print "Ack received ", ackNum
            else:
                print(data)
        
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

