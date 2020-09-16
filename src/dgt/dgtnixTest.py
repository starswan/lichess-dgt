#!/usr/bin/python

## dgtnix.py,  a test program for the dgtnix driver python bindings,
## Copyright (C) 2007 Pierre Boulenguez

## dgtnix, a POSIX driver for the Digital Game Timer chess board and clock
## Copyright (C) 2006-2007 Pierre Boulenguez

## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


import sys
import os
import errno
import time
import select

from dgtnix import *

# Load the library
try:
    dgtnix = dgtnix("libdgtnix.so")
except DgtnixError as e:
    print("unable to load the librairie : %s " % e)
    sys.exit()

print("dgtnixTest.py is a test Program for the dgtnix driver python bindings.")
print("This is dgtnix version %s " % dgtnix.QueryString(dgtnix.DGTNIX_DRIVER_VERSION))

if len(sys.argv)!= 2:
 print("usage: ./dgtnixTest.py port")
 print("Port is the port to which the board is connected.")
 print("For usb connection, try : /dev/ttyUSB0, /dev/usb/tts/0, /dev/usb/tts/1, /dev/usb/tts/2 ...")
 print("For serial, try : /dev/ttyS0, /dev/ttyS1, /dev/ttyS2 ...")
 print("For the virtual board /tmp/dgtnixBoard is the default but you can change it.")
 sys.exit()

# Turn debug mode to level 2
# all debug informations are printed
dgtnix.SetOption(dgtnix.DGTNIX_DEBUG, dgtnix.DGTNIX_DEBUG_ON)
# Initialize the driver with port argv[1]
board_pipe=dgtnix.Init(bytes(sys.argv[1], 'utf-8'))
if board_pipe < 0:
    print("Unable to connect to the device on "+sys.argv[1])
    sys.exit()
print("The board was found")
poll_obj = select.poll()
poll_obj.register(board_pipe)
dgtnix.update()
print(dgtnix.getFen('w').decode('utf-8'))
#board_out = ""
#dgtnix.SendToClock("tall  ", True, False)
while True:
    message = ""
    # print(dgtnix.getFen('w'))
    # time.sleep(1)
    events = poll_obj.poll(1000)
    if len(events) > 0:
        msg_type = ord(os.read(board_pipe, 1))

        if msg_type == dgtnix.DGTNIX_MSG_MV_ADD:
            file = os.read(board_pipe, 1).decode("utf-8")
            rank = ord(os.read(board_pipe, 1))
            piece = os.read(board_pipe, 1).decode("utf-8")
            print("Engine received DGTNIX_MSG_MV_ADD (" + piece + " on " + file + str(rank) + ")")
            print(dgtnix.getFen('w').decode('utf-8'))
        elif msg_type == dgtnix.DGTNIX_MSG_MV_REMOVE:
            file = os.read(board_pipe, 1).decode("utf-8")
            rank = ord(os.read(board_pipe, 1))
            piece = os.read(board_pipe, 1).decode("utf-8")
            print("Engine received DGTNIX_MSG_MV_REMOVE (" + piece + " on " + file + str(rank) + ")")
            print(dgtnix.getFen('w').decode('utf-8'))
        else:
            print("Engine Received unknown Message type " + msg_type.decode("utf-8"))

dgtnix.Close()

