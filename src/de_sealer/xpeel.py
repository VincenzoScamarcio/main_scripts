#!/usr/bin/env python

import serial


#xpeel = serial.Serial(port='COM6', baudrate=9600) #this works in python 3.8 windows
xpeel = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)

def set_param():
    #input = 'sealstat'
    input = 'stat'
    #input = 'sealcheck'
    #input = 'platecheck'

    xpeel.write(str.encode('*' + input + '\n\r'))
    response = xpeel.readline()
    print(response)

    return response #that's probably useless

def run():
    input = 'xpeel:41'

    xpeel.write(str.encode('*' + input + '\n\r'))
    response = xpeel.readline()
    print(response)
    response = xpeel.readline()
    print(response)

    return response #that's probably useless

if __name__ == "__main__":
    run()
