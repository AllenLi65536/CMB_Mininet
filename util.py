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
    for i in range(0,chunkSize,3):
        temp = []
        j = 0
        while i+j < len(data) or j == 3:
            temp.append(data[i+j])
        result.append(temp)
    return result
    '''

    result = []
    file = open(fileName, 'rb')
    return file.read()

    
    return blocksOfFile

def saveFileFromChunks(blocksOfFile, fileName):
    # TODO Save chunks into file
    return 0

def toByte(data):
    return data.encode('utf-8')

def toString(data):
    return data.decode('utf-8')


class Packet:
    def __init__(self, seq, ack, isSyn, isAck):
        self.seq = seq
        self.ack = ack
        self.isSyn = isSyn
        self.isAck = isAck
