import socket
import util
import sys
import time
import multiprocessing

def ReceiveHeartbeat(LocalIP, LocalPort, RemoteIP, RemotePort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sock.bind((LocalIP, LocalPort))
    sock.settimeout(10)

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data.startswith("HeartBeat"):
                #print "HeartBeat Received"
                wifiConnected = True
            else:
                print data
        except socket.timeout:
            #print "Receive Heartheat timeout"
            wifiConnected = False

def SendHeartbeat(LocalIP, LocalPort, RemoteIP, RemotePort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sock.bind((LocalIP, LocalPort))

    while True:
        sock.sendto("HeartBeat", (RemoteIP, RemotePort))
        time.sleep(4)

if __name__ == '__main__':

    RemoteIPH = "10.1.0.2" # High bandwidth
    RemoteIP = "10.0.0.2" # Low bandwidth

    LocalIPH = "10.1.0.3" # High bandwidth
    LocalIP = "10.0.0.3" # Low bandwidth
    SendPort = 5005
    ReceivePort = 5006

    sockS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sockS.bind((LocalIP, SendPort))
    
    sockSH = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sockSH.bind((LocalIPH, SendPort))
    
    sockR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sockR.bind((LocalIP, ReceivePort))
    
    sockRH = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sockRH.bind((LocalIPH, ReceivePort))

    wifiConnected = False
    
    # Start Heartbeat
    p1 = multiprocessing.Process(target=SendHeartbeat, args=(LocalIPH, 5010, RemoteIPH, 5009))
    p1.start()
    p2 = multiprocessing.Process(target=ReceiveHeartbeat, args=(LocalIPH, 5009, RemoteIPH, 5010))
    p2.start()

    while True:
        fileName, addr = sockR.recvfrom(1024) # buffer size is 1024 bytes
        print "requested file:", fileName

        #fileLength = 15 #Temporary
        #blocksOfFile = [str(i) + " " + str(i) for i in range(fileLength)] #Temporary
        
        blocksOfFile = util.getFileChunks(fileName)
        fileLength = len(blocksOfFile)
        
        #sock.sendto("Ack " + str(fileLength), (addr[0], addr[1])) # RemoteIP, RemotePort
        sockS.sendto("Ack " + str(fileLength), (RemoteIP, ReceivePort))

        #TODO send file
        print "Sending file"

        for i in range(fileLength):
            sockS.sendto(blocksOfFile[i], (RemoteIP, ReceivePort)) # Temporary
        
            # Receive ACK
#            while True:
#                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#                if data.startswith("Ack"):
#                    ackNum = int(data.split(" ")[1])
#                    print "Ack received ", ackNum
#                    break
#                else:
#                    print data
#


        print "Send file completed"




    # FOLLOWINGS ARE FOR REFERENCE ONLY NOT USED!!

    # SimpleHTTPServer
    #import SimpleHTTPServer
    #import SocketServer
    #
    #PORT = 8000
    #
    #Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    #
    #httpd = SocketServer.TCPServer(("", PORT), Handler)
    #
    #print "serving at port", PORT
    #httpd.serve_forever()
    #
    #
    ## FTP SERVER
    ## https://github.com/giampaolo/pyftpdlib
    #from pyftpdlib import servers
    #from pyftpdlib.handlers import FTPHandler
    #
    #address = ("0.0.0.0", 21)  # listen on every IP on my machine on port 21
    #
    #server = servers.FTPServer(address, FTPHandler)
    #server.serve_forever()

