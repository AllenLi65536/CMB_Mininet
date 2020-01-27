import multiprocessing

import random #temporary

CHUNK_SIZE = 1000

def getFileChunks(fileName, chunkSize = 1000):
    # Openfile and return chunks of file
    
    result = []
    file = open(fileName, 'rb')
    
    data = file.read()
    i = 0
    while i < len(data):
        temp = []
        j = 0
        while i+j < len(data) and j < chunkSize:
            temp.append(data[i+j])
            j += 1
        result.append(temp)
        i += j
    
    file.close()
    
    return result
    
def saveFileFromChunks(blocksOfFile, fileName):
    #print(getFileChunks(fileName)) # DEBUG
    fileName = fileName.strip("\n")
    newname = fileName.split('.')[0] + '_copy.' + fileName.split('.')[1]
    file = open(newname, 'wb')
    print("-------------------File saved------------------------------")
    #print(blocksOfFile) # DEBUG
    
    for block in blocksOfFile:
        try:
            for byte in block:
                file.write(byte)
        except:
            break
    file.close()

def toByte(data):
    return data.encode('utf-8')

def toString(data):
    return data.decode('utf-8')

def intToBytes(value, length):
    result = []

    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()

    return bytearray(result)

def bytesToInt(bytes):
    result = 0

    for b in bytes:
        result = result * 256 + int(b)
    return result

def getPacket(isAck, seqNumber, data = None):
    #print "seqNum: ", str(seqNumber)
    seq = bytes(str(seqNumber).zfill(10))
    #seq = intToBytes(seqNumber, 10)
    #seq = bytes(seqNumber)
    
    if isAck:
        return bytes(0) + seq
    else:
        return bytes(1) + seq + bytearray(data)

def getValueFromPacket(packet):
    #seqNum = bytesToInt(packet[1:11])
    seqNum = int(packet[1:11])
        
    if int(packet[0]) == 1:
        #isNotAck
        return (False, seqNum, packet[11:])
    else:
        return (True, seqNum, seqNum)

# Following codes are for reference only, not used
class Packet:
    def __init__(self, seq, ack, isSyn, isAck):
        self.seq = seq
        self.ack = ack
        self.isSyn = isSyn
        self.isAck = isAck
def RecvACKprocess(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        if data == "Ack":
            print("Ack received")
            break
def RecvACK(sock):
    p = multiprocessing.Process(target=RecvACKprocess, args=(sock,))
    p.start()
    p.join(1)
    # If process is still active, we kill it
    if p.is_alive():
      p.terminate()
      p.join()    
