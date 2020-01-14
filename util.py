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

    fileLength = random.randint(1,30) #Temporary
    blocksOfFile = [str(i) + " " + str(i) for i in range(fileLength)] #Temporary
    
    return blocksOfFile

def saveFileFromChunks(blocksOfFile, fileName):
    # TODO Save chunks into file
    return 0


class Packet:
    def __init__(self, seq, ack, isSyn, isAck):
        self.seq = seq
        self.ack = ack
        self.isSyn = isSyn
        self.isAck = isAck
