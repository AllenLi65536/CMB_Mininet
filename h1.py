# This file contains some possibility in implementation
# UDP Socket is preferred

# UDP Socket Send
#import socket
# 
#UDP_IP = "10.1.0.2" # High bandwidth
#UDP_IP = "10.0.0.2" # Low bandwidth
#UDP_PORT = 5005
#MESSAGE = "Hello, World!"
#print "UDP target IP:", UDP_IP
#print "UDP target port:", UDP_PORT
#print "message:", MESSAGE
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
#sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

#UDP Socket Receive

import socket
import util

#UDP_IP = "10.1.0.3" # High bandwidth
UDP_IP = "10.0.0.3" # Low bandwidth
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data



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

