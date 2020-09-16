from dgt.dgtnix import *

import select
import chess

class DgtBoard:
    def __init__(self, portname):
        self.__dgtdrv = dgtnix("libdgtnix.so")
        # Turn debug mode to level 2
        # all debug informations are printed
        self.__dgtdrv.SetOption(dgtnix.DGTNIX_DEBUG, dgtnix.DGTNIX_DEBUG_ON)
        self.__pipe = self.__dgtdrv.Init(bytes(portname, 'utf-8'))
        if self.__pipe < 0:
            raise "Unable to connect to the device on " + portname
        print("The board was found")
        self.__poll_obj = select.poll()
        self.__poll_obj.register(self.__pipe)
        self.__dgtdrv.update()
        print(self.__dgtdrv.getFen('w').decode('utf-8'))

    def new_game(self):
        self.__chessboard = chess.Board()
        self.__mystate = "init"

    # state appears to be either 'init' or 'myturn'
    def set_state(self, state):
        self.__mystate = state

    def get_state(self):
        return self.__mystate

    def get_user_move(self):
        pass

    def set_board_from_fen(self, fen):
        self.__chessboard = chess.Board(fen)

    def set_reference(self, reference):
        self.__reference = reference

    def get_reference(self):
        return self.__reference

    def get_color(self):
        return self.__color

    def set_color(self, color):
        self.__color = color

    def Close(self):
        self.__dgtdrv.Close()