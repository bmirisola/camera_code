import math
import os
import time

import cv2
import numpy as np

import Settings
import util.Constants as Constants
from util import Distance
from util.Polygon import Polygon
from util.UDPCannon import UDPCannon

# Creates a video capture object
# noinspection PyArgumentList
capture_source = cv2.VideoCapture(Constants.camera_port)

# Delays camera startup
time.sleep(1)

# Runs shell script to set camera configuration
os.system("scripts/configure.sh")

# Creates socket object to send values over
socket = UDPCannon("10.0.11.2", 8090)

# Tape contour array hold approximated polygons
tape_contour = []

# Boolean for 2 polygons detected
hasRun = False

# Hold midpoint of two tapes
center = []

# Holds value
meters = 0
angle_rads = 0
angle_deg = 0

high = 0
sec = 0
tapes = [None] * 2


# detects double left click and stores the coordinates in px
# This is for calibrating pixel values of retro tape so that everything can be blocked out
def print_hsv_at_coord(event, x, y, empty, data):
    global hsv
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print hsv[y, x]


# Sets print_hsv_at_coord function frame titled 'orig'
cv2.namedWindow('hsv')
cv2.setMouseCallback('hsv', print_hsv_at_coord)

# Calibrated HSV Ranges
# BGR
lower_green_thresh = np.array([Constants.low_blue, Constants.low_green, Constants.low_red])
upper_green_thresh = np.array([Constants.upper_blue, Constants.upper_green, Constants.upper_red])

# Starts video capture
# Creates two video windows. One from camera feed. Other blacks out everything not between calibrated BGR ranges
while True:
    ret, frame = capture_source.read()
    # frame = cv2.flip(frame, 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green_thresh, upper_green_thresh)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    # res = cv2.flip(res,0)

    # finds contours
    im2, contours, heirarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Creates two polygon objects
    for c in range(0, len(contours)):
        if cv2.contourArea(contours[c]) > cv2.contourArea(contours[high]):
            sec = high
            high = c
        elif (cv2.contourArea(contours[c]) > cv2.contourArea(contours[sec]) and cv2.contourArea(
                contours[c]) <= cv2.contourArea(contours[high])):
            sec = c

    top_tape = Polygon(frame, mask)
    bottom_tape = Polygon(frame, mask)

    # Runs bottom tape when contours is > 1
    if len(contours) > 0:
        bottom_tape.run(contours[high])

    # Runs top tape when contour count is > 2
    if len(contours) > 1:
        top_tape.run(contours[sec])
        hasRun = True

    # Finds center is two objects are found
    if hasRun:
        top_tape.center = list(top_tape.center)
        bottom_tape.center = list(bottom_tape.center)
        center = int((top_tape.center[0] + bottom_tape.center[0]) / 2), int(
            (top_tape.center[1] + bottom_tape.center[1]) / 2)
        center = list(center)
        horizontal_distance = Distance.find_distance(Constants.fake_focal, 4, bottom_tape.radius)
        if horizontal_distance != 0:
            angle_rads = math.atan(Constants.gear_peg_with_tape_length / horizontal_distance)
            angle_deg = math.degrees(angle_rads)
            angle_deg = math.ceil(angle_deg)
            if center[0] < 320:
                angle_deg = -angle_deg

        print 'Angle {0} | H. Distance {1}'.format(angle_deg, horizontal_distance)

    try:
        socket.send_target(angle_deg)
    except Exception as e:
        print "Can't connect : {0}".format(e)

    # Display windows if not in production mode
    if not Settings.PRODUCTION_MODE:
        # Shows Frames
        cv2.imshow('orig', frame)
        cv2.imshow('mask', mask)
        cv2.imshow('res', res)
        cv2.imshow("hsv", hsv)

    # Sets all values back to default
    hasRun = False
    bottom_tape.center = []
    top_tape.center = []
    center = []
    horizontal_distance = 0
    angle_rads = 0
    angle_deg = 0
    bottom_tape.high = 0
    top_tape.high = 0
    bottom_tape.sec = 0
    top_tape.sec = 0
    high = 0
    sec = 0

    # Shortcut for termination if not in production mode
    if not Settings.PRODUCTION_MODE:
        # Waits for q key to interrupt
        k = cv2.waitKey(20) & 0xFF
        if k == ord('q'):
            break

# Exits
capture_source.release()  # Release camera object
cv2.destroyAllWindows()  # Close all windows
