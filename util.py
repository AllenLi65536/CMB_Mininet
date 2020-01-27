import multiprocessing

import random #temporary

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

def getFileChunks(fileName, chunkSize = 1000):
    # TODO openfile and return chunks of file


    '''
    version 1
    result = []
    file = open(fileName, 'rb')
    data = file.read()
    i = 0
    while i < len(data):
        temp = []
        j = 0
        while i+j < len(data) and j <= chunkSize:
            temp.append(data[i+j])
            j += 1
        result.append(temp)
        i += j
    return result
    '''
    print('file name: ' + fileName[:-1]) #remove \n
    file = open(fileName[:-1], 'rb')
    # TODO Problem: this is not correct
    data = file.read()
    file.close()
    return data

def saveFileFromChunks(blocksOfFile, fileName):
    print(getFileChunks(fileName))
    newname = fileName.split('.')[0] + '_copy.' + fileName.split('.')[1]
    file = open(newname, 'wb')
    print("--------------------------------------------------------------")
    print(blocksOfFile)
    for i in blocksOfFile:
        # TODO Problem: write only one byte!?
        file.write(i[0])
    file.close()

def toByte(data):
    return data.encode('utf-8')

def toString(data):
    return data.decode('utf-8')

def getPacket(isAck, seqNumber, data = None):
    # TODO Problem: bytes(seqNumber) might not have same length
    if isAck:
        return bytes(0) + bytes(seqNumber)
    else:
        return bytes(1) + bytes(seqNumber) + data

def getValueFromPacket(packet):
    # TODO Problem: data only one byte!?
    data = packet[-1]
    if int(packet[0]) == 1:
        #isNotAck
        # TODO Problem seqNum might have more than one byte
        return (False, int(packet[1:-1]), packet[-1])
    else:
        # TODO Problem seqNum might have more than one byte
        return (True, packet[0], int(packet[1:]))




class Packet:
    def __init__(self, seq, ack, isSyn, isAck):
        self.seq = seq
        self.ack = ack
        self.isSyn = isSyn
        self.isAck = isAck
