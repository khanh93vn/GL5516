# -*- coding: UTF-8 -*-

from sys import exit
from time import ctime, time, localtime, sleep
from struct import unpack
from numpy import array
from serial import Serial

# ----------------------------------------------------------------------------
# Constants

BAUDRATE = 115200
TIMEOUT = 5
BUFFERSIZE = 100
READSIZE = BUFFERSIZE*2
BUFFERFORMAT = str(BUFFERSIZE) + 'H'
    
# ----------------------------------------------------------------------------
# Main
if __name__ == "__main__":
    # Read port from keyboard:
    port = input("Enter connected port (for example: COM4, COM5, ...): ")

    # Start connection:
    stream = Serial(port, BAUDRATE, timeout=TIMEOUT)
    try:
        print(stream.readline().decode())
    except: # stop serial communication if something is wrong
        stream.flushOutput()
        stream.flushInput()
        stream.close()
        print("Something is wrong with the connection...")
        exit()
    
    print("System starting...\n")
    
    timeinfo = array(localtime(0.0), dtype='int32')
    timeinfo.tofile("time.info")
    
    # Main loop:
    while True:
        stream.write('m'.encode())
        
        # Receive:
        Vout1 = array(unpack(BUFFERFORMAT,
                             stream.read(READSIZE)),
                      dtype='uint16')
        Vout2 = array(unpack(BUFFERFORMAT,
                             stream.read(READSIZE)),
                      dtype='uint16')
        
        # Save to file:
        now = time()
        Vout1.tofile("Vout1_" + str(now) + ".dat")
        Vout2.tofile("Vout2_" + str(now) + ".dat")
        
        # Display output:
        print(ctime(now)
              + "... Measured V_outs:\n%d\n%d\n..."
                %(Vout1.mean(), Vout2.mean()))
        
        sleep(60.0)
        
    stop(stream)