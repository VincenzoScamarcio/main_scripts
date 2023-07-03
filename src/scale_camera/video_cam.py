#!/usr/bin/env python

import cv2
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc

# open the webcam video stream
cam_port = 1
webcam = cv2.VideoCapture(1)  #0 for PC webcam, 1 for external webcam

#main loop
while True:
    # get the frame from the webcam
    stream_ok, frame = webcam.read()

    # if webcam stream is ok
    if stream_ok:
        #display current frame
        cv2.imshow('Webcam', frame)

    # escape condition
    if cv2.waitKey(1) & 0xFF == 27: break

#clean ups
cv2.destroyAllWindows()

#release webcam stream
webcam.release()