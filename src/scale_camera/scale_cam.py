#!/usr/bin/env python

import serial
import time
import csv
from statistics import mean
import cv2
import os

scale = serial.Serial(port='COM7', baudrate=115200, timeout=.1)

def scale():
    time.sleep(0.1)

    #read & record data
    data = []                       # empty list to store the data
    for i in range(50):
        b = scale.readline()         # read a byte string
        string_n = b.decode()        # decode byte string into Unicode
        string = string_n.rstrip()   # remove \n and \r

        try:                         #needed because Arduino & Python are not syncronized
            flt = float(string)        # convert string to float
            #print(flt)                 #-153.54 if you don't wanna tare the scale evey time
            data.append(flt-154.39)     # add to the end of data list
            #time.sleep(0.1)           # wait (sleep) 0.1 seconds
        except:                        #just do nothing, the data=[] will have less values
            print(string)
            #print('exception')

    scale.close()
    data.pop(0)
    for line in data:
        print(round(line, 1))     #if you don't wanna tare the scale at the beginning, you use  -153.5

    print(mean(data))
    print(len(data))

    m = [[mean(data)]]
    #header = ['Plate weight']

    with open('Images/Plate_weight.csv', 'a', encoding='UTF8', newline='') as file:     #'a' append mode can be switched to 'w' write mode to re-write the csv file
        writer = csv.writer(file)

        # write the header
        #writer.writerow(header)

        # write multiple rows
        writer.writerows(m)

def cam():
    # initialize the camera
    # If you have multiple camera connected with
    # current device, assign a value in cam_port
    # variable according to that
    cam_port = 1
    cam = cv2.VideoCapture(cam_port)

    # reading the input using the camera
    result, image = cam.read()
    cam.release()
    # If image will detected without any error,
    # show result
    if result:

        # showing result, it take frame name and image
        # output
        #cv2.imshow("GeeksForGeeks", image)

        # saving image in local storage
        path = 'C:/Users/scamarci/Documents/Automation project/Scale/Images'

        if not os.path.isdir(path):
            print(f"No such a directory: {path}")
            exit(1)


        n_files = next(os.walk('Images'))[2]  # Images is the directory file I wanna count is your directory path as string
        print (len(n_files))
        n = len(n_files) - 1
        cv2.imshow(f'plate{n:04}.jpg', image)
        cv2.imwrite(os.path.join(path, f'plate{n:04}.jpg'), image)
        # If keyboard interrupt occurs, destroy image
        # window
        cv2.waitKey(0)
        #cv2.destroyWindow("GeeksForGeeks")

    # If captured image is corrupted, moving to else part
    else:
        print("No image detected. Please! try again")

def cam_scale():
    scale()
    cam()

if __name__ == '__main__':
    scale()
