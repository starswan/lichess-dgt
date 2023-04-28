from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol, connectionDone
from twisted.python import failure
from twisted.web._newclient import ResponseDone

class WriteToStdout(Protocol):
    def __init__(self, prefix):
        self.__prefix = prefix
        self.onConnLost = None

    def connectionMade(self):
        self.onConnLost = Deferred()

    def dataReceived(self, data):
        """
        Print out the html page received.
        """
        print('%s Got %d bytes:[%s]' % (self.__prefix, len(data), data))

    def connectionLost(self, reason: failure.Failure = connectionDone):
        if not reason.check(ResponseDone):
            reason.printTraceback()
        else:
            print(self.__prefix + ' Response done')
        self.onConnLost.callback(None)
