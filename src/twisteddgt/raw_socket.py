from twisted.internet import abstract, fdesc

class TwistedRawSocket(abstract.FileDescriptor):
    def __init__(self, reactor, protocol, fd):
        super().__init__(reactor)
        self.__protocol = protocol
        self.__protocol.makeConnection(self)
        self.__fd = fd
        self.startReading()

    def fileno(self):
        return self.__fd

    def doRead(self):
        return fdesc.readFromFD(self.fileno(), self.__protocol.dataReceived)

    def writeSomeData(self, data):
        return fdesc.writeToFD(self.fileno(), data)

    def connectionLost(self, reason):
        abstract.FileDescriptor.connectionLost(self, reason)
        self.__protocol.connectionLost(reason)
