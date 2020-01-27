import socket
import threading
import time
import sys
import util

#how to use: 
#app = FTPClient()
#app.run()


class FTPClient:
    def __init__(self):

        #global here
        self.fileBlockReceived = [False]
        self.fileBlocks = [0]
        self.fileLength = 0
        self.wifiConnected = False

        self.highBlocks = 0
        self.lowBlocks = 0

        self.remoteIPH = "10.1.0.3"
        self.remoteIP = "10.0.0.3"

        self.localIPH = "10.1.0.2"
        self.localIP = "10.0.0.2"

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
        self.sockRH.settimeout(0.5)

    def initHeartBeat(self):
        self.sendHeartBeatThread = threading.Thread(target=self.sendHeartbeat)
        self.recvHeartBeatThread = threading.Thread(target=self.receiveHeartbeat)
        self.sendHeartBeatThread.start()
        self.recvHeartBeatThread.start()

    def run(self):
        while True:
            print "Input request filename:",
            fileName = sys.stdin.readline()
            filName = fileName[:-1] # Remove \n
            self.fileLength = 0
            
            isTimeout = True
            while True:
                if isTimeout: 
                    self.sockS.sendto(fileName, (self.remoteIP, self.recvPort))
                    isTimeout = False
                try:
                    data,addr = self.sockR.recvfrom(1024)
                except socket.timeout:
                    isTimeout = True
                    continue
                
                # TODO use packet instead of plain string
                if data.startswith("Ack"):
                    # TODO use packet instead of plain string
                    self.fileLength = int(data.split(" ")[1]) # Temporary
                    print("Ack received, fileLength: " + str(self.fileLength))
                    break
                else:
                    isTimeout = False # Redundant line but easier to understand
                    
                    # Ack pending acks (Just double check)
                    # Use packet instead of plain string
                    data = util.getValueFromPacket(data)
                    seqNum = data[1]
                    packet = util.getPacket(True, seqNum)
                    #seqNum = int(data.split(" ")[0])  # Temporary
                    #self.sockS.sendto("Ack " + str(seqNum), (self.remoteIP, self.recvAckPort))
                    self.sockS.sendto(packet, (self.remoteIP, self.recvAckPort))
                    print(data)
            
            self.fileBlockReceived = [False] * self.fileLength
            self.fileBlocks = [0] * self.fileLength
            print("recving file")

            t1 = time.time()
        
            self.highBlocks = 0
            self.lowBlocks = 0

            lowChunkThread = threading.Thread(target=self.receiveFileChunks, args=(self.sockR, self.sockS, False))
            highChunkThread = threading.Thread(target=self.receiveFileChunks, args=(self.sockRH, self.sockSH, True))
            lowChunkThread.start()
            highChunkThread.start()

            lowChunkThread.join()
            highChunkThread.join()

            delta = time.time() - t1
            print("recv completed!")
            print("time elapsed: " + str(delta) + " seconds")
            print("speed: " + str(self.fileLength / delta) + "Blocks/second")
            print("Blocks sent through Wifi: " + str(self.highBlocks))
            print("Blocks sent through mobile network: " + str(self.lowBlocks))

            util.saveFileFromChunks(self.fileBlocks, fileName)
            
            
            # Ack pending acks
            time.sleep(1.5) # temporary
            while True:
                try:
                    data,addr = self.sockR.recvfrom(1024)
                except socket.timeout:
                   break
                
                data = util.getValueFromPacket(data)
                seqNum = data[1]
                packet = util.getPacket(True, seqNum)
                self.sockS.sendto(packet, (self.remoteIP, self.recvAckPort))
            
            while True:
                try:
                    data,addr = self.sockRH.recvfrom(1024)
                except socket.timeout:
                   break
              
                # Use packet instead of plain string
                data = util.getValueFromPacket(data)
                seqNum = data[1]
                packet = util.getPacket(True, seqNum)
                self.sockS.sendto(packet, (self.remoteIP, self.recvAckPort))
                #seqNum = int(data.split(" ")[0])  # Temporary
                #self.sockS.sendto("Ack " + str(seqNum), (self.remoteIP, self.recvAckPort))
    
    def receiveFileChunks(self, receiver, sender, isHighSpeed):
        while sum(self.fileBlockReceived) < self.fileLength:
            #print "blockCount:", sum(self.fileBlockReceived), " fileLength:", self.fileLength  # Temporary
            try:
                data, addr = receiver.recvfrom(1024)
            except socket.timeout:
                continue
            
            # Use packet instead of plain string
            data = util.getValueFromPacket(data)
            #print("data")
            #print(data)
            seqNum = data[1]
            packet = util.getPacket(True, seqNum)
            # Send ACK
            if isHighSpeed:
                # print "Received through Wifi ", str(seqNum)
                sender.sendto(packet, (self.remoteIPH, self.recvAckPort))
                self.highBlocks += 1
            else:
                sender.sendto(packet, (self.remoteIP, self.recvAckPort))
                self.lowBlocks += 1

            self.fileBlocks[seqNum] = data[2]
            self.fileBlockReceived[seqNum] = True


    def sendHeartbeat(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET, UDP
        sock.bind((self.localIP, 5010))

        while True:
            sock.sendto("H", (self.remoteIP, 5009))
            time.sleep(1)

    def receiveHeartbeat(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET, UDP
        sock.bind((self.localIP, 5009))
        sock.settimeout(15)

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if data.startswith("H"):
                    # print "HeartBeat Received"
                    self.wifiConnected = True
                else:
                    print data
            except socket.timeout:
                # print "Receive Heartheat timeout"
                self.wifiConnected = False


if __name__ == '__main__':

    app = FTPClient()
    app.run()

