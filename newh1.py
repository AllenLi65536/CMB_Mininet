import socket
import threading
import time
import sys
import util

#how to use: 
#app = FTPServer()
#app.run()


class FTPServer:
    def __init__(self):

        #global here
        self.fileBlockReceived = [False]
        self.fileBlocks = [0]
        self.fileLength = 0

        self.wifiConnected = False
        self.cv = threading.Condition()

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

        print "Server started"

        while True:
            try:
                fileName, addr = self.sockR.recvfrom(1024) # buffer size is 1024 bytes
            except socket.timeout:
                #print "Timeout" # Temp
                continue
            fileName = util.toString(fileName)
            fileName = fileName[:-1] # Remove \n
            print "requested file: ", fileName

            self.fileBlocks = util.getFileChunks(fileName)
            #print("blocks")
            #print(self.fileBlocks)
            self.fileLength = len(self.fileBlocks)
            self.fileBlockReceived = [False] * self.fileLength
            
            # Use plain string for simplicity here
            self.sockS.sendto("Ack " + str(self.fileLength), (self.remoteIP, self.recvPort))
            
            # Wait for RTT
            time.sleep(0.3) # temporary

            print "Sending file"

            #send file with multithread on multiple link

            sendFileThreadH = threading.Thread(target=self.sendFileChunksH, args=())
            sendFileThreadH.start()
            
            sendFileThread = threading.Thread(target=self.sendFileChunks, args=())
            sendFileThread.start()
                        
            sendFileThread.join()
            sendFileThreadH.join()
            
            print "Send file completed"

    #Send file through mobile network
    def sendFileChunks(self):
        firstIter = True
        while sum(self.fileBlockReceived) < self.fileLength:
            if not firstIter:
                # Wait for RTT
                time.sleep(0.5) # temporary
            firstIter = False
            
            for i in range(self.fileLength):
                if not self.fileBlockReceived[i]:
                    # Use packet instead of plain string 
                    packet = util.getPacket(False, i, self.fileBlocks[i])
                    self.sockS.sendto(packet, (self.remoteIP, self.recvPort))
    
    #Send file through wifi
    def sendFileChunksH(self):
        firstIter = True
        while sum(self.fileBlockReceived) < self.fileLength:
            if not firstIter:
                # Wait for RTT
                time.sleep(0.5) # temporary
            firstIter = False
            
            # Wait for Wifi
            while not self.wifiConnected:
                if sum(self.fileBlockReceived) >= self.fileLength:
                    return
                with self.cv:
                    self.cv.wait(0.5)
            
            for i in range(self.fileLength-1, -1, -1): # backward from fileLength-1 to 0
                if not self.fileBlockReceived[i]:
                    
                    # Wait for Wifi
                    #while not self.wifiConnected:
                    #    if sum(self.fileBlockReceived) >= self.fileLength:
                    #        return
                    #    with self.cv:
                    #        self.cv.wait(0.5)
                    
                    # Use packet instead of plain string
                    packet = util.getPacket(False, i, self.fileBlocks[i])
                    self.sockSH.sendto(packet, (self.remoteIPH, self.recvPort))

    def receiveAcks(self, sock):
        # Receive ACK
        while True:
            try:
                data, addr = sock.recvfrom(1024)
            except socket.timeout:
                continue
            result = util.getValueFromPacket(data)
            if result[0]:
                self.fileBlockReceived[int(result[2])] = True
                print "Ack received ", int(result[2])
            else:
                print(result)
            
        
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
                    with self.cv:
                        self.cv.notifyAll()
                else:
                    print data
            except socket.timeout:
                # print "Receive Heartheat timeout"
                self.wifiConnected = False


if __name__ == '__main__':

    app = FTPServer()
    app.run()

