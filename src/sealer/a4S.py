#!/usr/bin/env python

import serial
import time
import getpass

a4S = serial.Serial(port='/dev/ttyS3', baudrate=19200)

def set_param():
    input = 'DH=0182'   #+7 degrees in respect to temp you want to reach
    #input = 'DT=0050'  #deci-seconds, so 0010 means 1 sec
    a4S.write(str.encode('*00' + input + 'zz!'))

    #readout response does not work
    #print(1)
    #response = a4S.readline()
    #print(2)
    #print(response)

    #return response

def run():
    input = 'GS'
    a4S.write(str.encode('*00' + input + 'zz!'))
    time.sleep(15)

    # readout response does not work
    # print(1)
    # response = a4S.readline()
    # print(2)
    # print(response)

    # return response

if __name__ == "__main__":
    run()