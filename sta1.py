import socket
import util
import sys

readline = sys.stdin.readline
 
# UDP Socket Send
#UDP_IP = "10.1.0.3" # High bandwidth
SendIP = "10.0.0.3" # Low bandwidth
SendPort = 5005
#message = "Hello, World!"
#print "UDP target IP:", SendIP
#print "UDP target port:", UDP_PORT
#print "message:", message
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP

while True:
    message = readline()
    sock.sendto(message, (SendIP, SendPort))
    util.RecvACK(sock) 


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
