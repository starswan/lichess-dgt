from dgt.dgtnix import *

import select
# import chess

class DgtBoard:
    def __init__(self, portname):
        self.__dgtdrv = dgtnix("libdgtnix.so")
        # Turn debug mode to level 2
        # all debug information is printed
        self.__dgtdrv.SetOption(dgtnix.DGTNIX_DEBUG, dgtnix.DGTNIX_DEBUG_ON)
        self.__pipe = self.__dgtdrv.Init(bytes(portname, 'utf-8'))
        if self.__pipe < 0:
            raise "Unable to connect to the device on " + portname
        print("The board was found")
        self.__poll_obj = select.poll()
        self.__poll_obj.register(self.__pipe)
        self.__dgtdrv.update()
        print('FEN:' + self.__dgtdrv.getFen('w').decode('utf-8'))

    def pipe(self):
        return self.__pipe

    def Close(self):
        self.__dgtdrv.Close()