#
# The goal of chess.py is to control
# 1. the board
# 2. the beserk client
# 3. the user
#
# sp that they co-operate nicely

# import berserk
# import asyncio
# from lichess_client import APIClient
from serial import STOPBITS_ONE, PARITY_NONE, EIGHTBITS
from twisted.internet import reactor
from twisted.internet.serialport import SerialPort
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.web.iweb import UNKNOWN_LENGTH
from twisted import version
from twisted.python import log
from pprint import pprint
import dgt
# import sys

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
from dgt.board import DgtBoard
from twisteddgt.raw_protocol import RawBoardDataReceived
# from twisteddgt.raw_socket import TwistedRawSocket
from twisteddgt.write_to_stdout import WriteToStdout

GET_REQUEST = bytes('GET', 'utf-8')

def main(reactor, portname, tokenfile, url):
    dgtboard = DgtBoard(portname, False, False, False)

    with open(tokenfile) as f:
        token = f.read().strip()

    twisted_dgt = SerialPort(RawBoardDataReceived(dgtboard), portname, reactor, stopbits=STOPBITS_ONE, parity=PARITY_NONE, bytesize=EIGHTBITS)
    url = bytes(url + '/api/stream/event', 'utf-8')

    userAgent = 'Twisted/%s' % (version.short(),)
    auth = 'Bearer %s' % (token)
    agent = Agent(reactor)
    d = agent.request(
        GET_REQUEST, url, Headers({'User-Agent': [userAgent], 'Authorization': [auth]}))
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
    # main(reactor, portname='/dev/ttyUSB0', tokenfile='lichess.org.token', url='https://lichess.org')
    # or
    main(reactor, portname='/dev/ttyUSB0', tokenfile='lichess.dev.token', url='https://lichess.dev')
    # main(reactor, *sys.argv[1:], token)