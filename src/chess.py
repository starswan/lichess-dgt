#
# The goal of chess.py is to control
# 1. the board
# 2. the beserk client
# 3. the user
#
# sp that they co-operate nicely

import dgt
import berserk
# import asyncio
# from lichess_client import APIClient

dgtboard = dgt.DgtBoard(portname='/dev/ttyS0')

TOKEN_FILE='./lichess.token'
with open(TOKEN_FILE) as f:
    token = f.read().strip()

lichess = berserk.Client(berserk.TokenSession(token), base_url="https://lichess.dev")
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
for event in lichess.board.stream_incoming_events():
    pass