# -*- coding: UTF-8 -*-
"""
Code for LDR measurement with Arduino board.

Usage:
- Connect and upload measurement_ldr.ino to arduino board.
- Run script with interactive ipython and type
stream = start(<port connected*>) to start serial communication.
- Type a = adjustAndMeasure(stream, x) - with x in 0..255 - assign array of
measured values (at LED light intensity of x out of 255) to variable a.
- Close serial communication with stop(stream) when finish.

*: default is 'COM4'

*******************************************************************************
Code cho thi nghiem do quang tro bang Arduino

Cach su dung:
- Ket noi va nap code trong measurement_ldr.ino vao board Arduino.
- Chay script bang giao dien tuong tac ipython va go 
stream = start(<port connected>) de bat dau ket noi serial voi board Arduino.
- Go a = adjustAndMeasure(stream, x) - x nhan gia tri 8 bit - de nhan gia tri
do duoc o do sang LED x/255 (do nhieu lan).
- Ngat ket noi serial voi board Arduino bang cach go stop(stream).
"""

import serial
import numpy as np

from struct import unpack

# -----------------------------------------------------------------------------
# Constants

DEFAULTPORT = 'COM4' # adjusted according to connected port
BAUDRATE = 115200

BUFFERSIZE = 100
BUFFERFORMAT = str(BUFFERSIZE) + 'H'

VCC = 1023.0
RREF = 10000.0

# -----------------------------------------------------------------------------
# Functions

def start(port=DEFAULTPORT, baudrate=BAUDRATE):
    com = serial.Serial(port, baudrate, timeout=5)
    try:
        print(com.readline().decode())
    except: # stop serial communication if something is wrong
        stop(com)
        return None
    return com


def stop(com):
    com.flushOutput()
    com.flushInput()
    com.close()

def send(com, message):
    com.write("{0:04d}".format(message).encode())


def receive(com, size=BUFFERSIZE*2, format=BUFFERFORMAT):
    return np.array(unpack(format, com.read(size)), dtype='uint16')


def adjustAndMeasure(com, inp, size=BUFFERSIZE*2, format=BUFFERFORMAT):
    send(com, inp)
    return res(receive(com, size, format))

    
def res(Vout, Vcc=VCC, Rref=RREF):
    return Rref * (Vcc - Vout) / Vout

# -----------------------------------------------------------------------------
# Main

if __name__ == "__main__":
    # Start serial communication:
    # stream = start(DEFAULTPORT, BAUDRATE)

    # Close communication:
    # stop(stream)
    
    pass