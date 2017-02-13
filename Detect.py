import math
import numpy as np
import os
import time

import cv2

import Constants
import Distance
from Polygon import Polygon
from UDPCannon import UDPCannon

# Creates a video capture object
vid = cv2.VideoCapture(Constants.camera_port)

# delays camera startup
time.sleep(1)

#Runs shell script to start camera configuration
os.system("scripts/configure.sh")

#Creates socket object to send values over
socket = UDPCannon("10.0.11.67", 8090)

#Tape contour array hold approximated polygons
tape_contour = []

#Boolean for 2 polygons detected
hasRun = False

# hold midpoint of two tapes
center = []

# holds distance value
distance = 0
meters = 0

# detects double left click and stores the coordinates in px
# This is for calibrating pixel values of retro tape so that everything can be blocked out
def printpix(event, x, y, flags, params):
    global hsv
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print hsv[y, x]


# Sets printpix function frame titled 'orig'
cv2.namedWindow('hsv')
cv2.setMouseCallback('hsv', printpix)

# Calibrated HSV Ranges
# BGR
lower_green = np.array([Constants.low_blue, Constants.low_green, Constants.low_red])
upper_green = np.array([Constants.upper_blue, Constants.upper_green, Constants.upper_red])

# Starts video capture
# Creates two video windows. One from camera feed. Other blacks out everything not between calibrated BGR ranges
while (True):
    ret, frame = vid.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    #finds contours
    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #Creates two polygon objects
    top_tape = Polygon(frame, mask)
    bottom_tape = Polygon(frame, mask)

    #Runs bottom tape when contours is > 1
    if (len(contours) > 0):
        bottom_tape.run(contours[0])

    #Runs top tape when contour count is > 2
    if (len(contours) > 1):
        top_tape.run(contours[1])
        hasRun = True

    #Finds center is two objects are found
    if (hasRun):
        top_tape.center = list(top_tape.center)
        bottom_tape.center = list(bottom_tape.center)
        center = int((top_tape.center[0] + bottom_tape.center[0]) / 2), int(
            (top_tape.center[1] + bottom_tape.center[1]) / 2)
        center = list(center)

    print ('The center of bottom tape is ' + str(bottom_tape.center))
    print ('The center of top tape is ' + str(top_tape.center))
    print ('The center is ' + str(center))

    # print Distance.focal_length(bottom_tape.radius,2,158)
    # Finds horizontal distance
    HorizontalDistance = Distance.find_distance(1659, 2, bottom_tape.radius)
    print HorizontalDistance
    distance = math.sqrt(math.pow(HorizontalDistance, 2) + math.pow(Constants.BolierHeight, 2))
    #Sends center over as a String array
    try:
        socket.put("centerX", str(center))
    except Exception as e:
        print "Can't connect : {0}".format(e)

    #Shows Frames
    cv2.imshow('orig', frame)
    # cv2.imshow('mask', mask)
    # cv2.imshow('res', res)
    #cv2.imshow("hsv", hsv)

    #Sets all values abck to default
    hasRun = False
    bottom_tape.center = []
    top_tape.center = []
    center = []

    #Waits for q key to interupt
    k = cv2.waitKey(20) & 0xFF
    if k == ord('q'):
        break

# exits
vid.release()
cv2.destroyAllWindows()