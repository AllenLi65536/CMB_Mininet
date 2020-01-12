import socket
import util

wifiConnected = False

def ReceiveHeartbeat(LocalIP, LocalPort, RemoteIP, RemotePort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sock.bind((LocalIP, LocalPort))
    sock.settimeout(10)

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data.startswith("HeartBeat"):
                global wifiConnected
                wifiConnected = True
        except socket.timeout:
            print "Receive Heartheat timeout"
            global wifiConnected
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
    RemotePort = 5005

    LocalIPH = "10.1.0.3" # High bandwidth
    LocalIP = "10.0.0.3" # Low bandwidth
    LoaclPort = 5005

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sock.bind((LocalIP, LoaclPort))
    
    # Start Heartbeat
    p = multiprocessing.Process(target=SendHeartbeat, args=(LocalIP, 5010, RemoteIP, 5009))
    p.start()
    p = multiprocessing.Process(target=ReceiveHeartbeat, args=(LocalIP, 5009, RemoteIP, 5010))
    p.start()

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print "requested file:", data
        sock.sendto("Ack 15", (addr[0], addr[1])) # RemoteIP, RemotePort

        #TODO send file
        print "Sending file"


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

