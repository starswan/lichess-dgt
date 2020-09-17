#
# The goal of chess.py is to control
# 1. the board
# 2. the beserk client
# 3. the user
#
# sp that they co-operate nicely

import dgt.dgt
import berserk
# import asyncio
# from lichess_client import APIClient
from twisted.internet import reactor, abstract, fdesc
from twisted.web.client import Agent, ResponseDone
from twisted.internet.protocol import Protocol
from twisted.internet.defer import Deferred
from twisted.web.http_headers import Headers
from twisted.web.iweb import UNKNOWN_LENGTH
from twisted import version
from twisted.python import log
from pprint import pprint
import sys

# lichess = berserk.Client(berserk.TokenSession(token), base_url="https://lichess.dev")
# async def main():
#     client = APIClient(token=token)
#     response = await client.account.get_my_profile()
#     print(response)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

# This is a bit annoying - when it is our turn (and maybe otherwise too)
# we need to be looking at the board for moves - so we need to do both
# The async client was crap as it didn't let us override the lichess.org URL to be lichess.dev for testing...
# I think beserk doesn't really do enough. It does gets and posts and de-serialises thw JSON result,
#'and a tiny bit of OAuth2 helper header: 'Authentication: 'Bearer #{token}' but that's it.
# asyncio would have been better, but doesn't allow override of the host name
# Think I need to look at twisted.
# for event in lichess.board.stream_incoming_events():
#     pass
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

class TwistedRawSocket(abstract.FileDescriptor):
    def __init__(self, reactor, protocol, fd):
        super().__init__(reactor)
        self.__protocol = protocol
        self.__protocol.makeConnection(self)
        self.__fd = fd
        # self.reactor.addReader(fd)
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

def main(reactor):
    dgtboard = dgt.dgt.DgtBoard(portname='/dev/ttyUSB0')

    TOKEN_FILE='./lichess.org.token'
    with open(TOKEN_FILE) as f:
        token = f.read().strip()

    twisted_dgt = TwistedRawSocket(reactor, WriteToStdout('Board:'), dgtboard.pipe())
    url = bytes('https://lichess.org/api/stream/event', 'utf-8')

    """
    We create a custom UserAgent and send a GET request to a web server.
    """
    userAgent = 'Twisted/%s' % (version.short(),)
    auth = 'Bearer %s' % (token)
    agent = Agent(reactor)
    d = agent.request(
        bytes('GET', 'utf-8'), url, Headers({'user-agent': [userAgent], 'Authorization': [auth]}))
    def cbResponse(response):
        """
        Prints out the response returned by the web server.
        """
        pprint(vars(response))
        proto = WriteToStdout('URL:')
        if response.length is not UNKNOWN_LENGTH:
            print('The response body will consist of', response.length, 'bytes.')
        else:
            print('The response body length is unknown.')
        response.deliverBody(proto)
        return proto.onConnLost
    d.addCallback(cbResponse)
    d.addErrback(log.err)
    d.addBoth(lambda ign: reactor.callWhenRunning(reactor.stop))
    reactor.run()

if __name__ == '__main__':
    main(reactor)
    # main(reactor, *sys.argv[1:], token)