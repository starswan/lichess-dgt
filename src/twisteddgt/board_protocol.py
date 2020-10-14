from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web._newclient import ResponseDone

from dgtc.dgtnix import dgtnix

class WriteToStdout(Protocol):
    def __init__(self, prefix):
        self.__prefix = prefix

    def connectionMade(self):
        self.onConnLost = Deferred()

    def dataReceived(self, data):
        """
        Print out the html page received.
        """
        print('%s Got %d bytes:[%s]' % (self.__prefix, len(data), data))

    def connectionLost(self, reason):
        if not reason.check(ResponseDone):
            reason.printTraceback()
        else:
            print(self.__prefix + ' Response done')
        self.onConnLost.callback(None)

class BoardDataReceived(Protocol):
    def __init__(self, client):
        self.__client = client

    def dataReceived(self, data):
        print('Got %d bytes:[%s]' % (len(data), data))
        if data[0] == dgtnix.DGTNIX_MSG_MV_ADD:
            file = chr(data[1])
            rank = data[2]
            piece = chr(data[3])
            print("Engine received DGTNIX_MSG_MV_ADD (%s on %s%d)" % (piece, file, rank))
            # self.__client.pieceAdded(piece, rank, file)
        elif data[0] == dgtnix.DGTNIX_MSG_MV_REMOVE:
            file = chr(data[1])
            rank = data[2]
            piece = chr(data[3])
            print("Engine received DGTNIX_MSG_MV_REMOVE (%s on %s%d)" % (piece, file, rank))
            # self.__client.pieceRemoved(piece, rank, file)
