from twisted.internet.protocol import Protocol
from dgtc.dgtnix import dgtnix

class BoardDataReceived(Protocol):
    def __init__(self, client):
        self.__client = client

    def dataReceived(self, data):
        print('BOARD: Got %d bytes:[%s]' % (len(data), data))
        message_type = data[0]
        if message_type == dgtnix.DGTNIX_MSG_MV_ADD:
            file = chr(data[1])
            rank = data[2]
            piece = chr(data[3])
            print("BOARD: received DGTNIX_MSG_MV_ADD (%s on %s%d)" % (piece, file, rank))
            # self.__client.pieceAdded(piece, rank, file)
        elif message_type == dgtnix.DGTNIX_MSG_MV_REMOVE:
            file = chr(data[1])
            rank = data[2]
            piece = chr(data[3])
            print("BOARD: received DGTNIX_MSG_MV_REMOVE (%s on %s%d)" % (piece, file, rank))
        else:
            print("Board: received undecoded message %d" % (message_type))
            # self.__client.pieceRemoved(piece, rank, file)
