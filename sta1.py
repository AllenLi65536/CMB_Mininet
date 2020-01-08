import socket
import util
import sys
import time
import multiprocessing

readline = sys.stdin.readline

def SendHeartbeat(LocalIP, LocalPort, SendIP, SendPort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sock.bind((LocalIP, LocalPort))

    #TODO Recv heartbeat
    
    while True:
        sock.sendto("HeartBeat", (SendIP, SendPort))
        time.sleep(4)
 
if __name__ == '__main__':

    # UDP Socket Send
    #SendIP = "10.1.0.3" # High bandwidth
    SendIP = "10.0.0.3" # Low bandwidth
    SendPort = 5005
    
    #LocalIP = "10.1.0.2" # High bandwidth
    LocalIP = "10.0.0.2" # Low bandwidth
    LocalPort = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sock.bind((LocalIP, LocalPort))
    
    p = multiprocessing.Process(target=SendHeartbeat, args=(LocalIP, LocalPort, SendIP, SendPort))
    p.start()

    while True:
        print("Input request filename:"),
        message = readline()
        sock.sendto(message, (SendIP, SendPort))
        #util.RecvACK(sock) 
        
        while True:
            data, addr = sock.recvfrom(1024)
            if data.startswith("Ack"):
                fileLength = int(data.split(" ")[1])
                print "Ack received, fileLength: ", fileLength
                break
        
        # TODO Receive file
        print "Receiving file..."
        
        time.sleep(fileLength)
        print "Receive completed!"


    #UDP Socket Receive
    #
    #UDP_IP = "10.1.0.2" # High bandwidth
    #UDP_IP = "10.0.0.2" # Low bandwidth
    #UDP_PORT = 5005
    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    #sock.bind((UDP_IP, UDP_PORT))
    #
    #while True:
    #    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #    print "received message:", data
