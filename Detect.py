import numpy as np
import os
import time

import cv2

import Constants
from UDPCannon import UDPCannon

vid = cv2.VideoCapture(Constants.camera_port)
time.sleep(1)

os.system("scripts/configure.sh")
socket = UDPCannon("10.0.11.67", 8090)
tape_contour = []


# top_tape = Polygon(frame, mask)
# bottom_tape = Polygon(frame, mask)

# im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# top_tape = Polygon.make_polygon(top_tape, frame, mask)
# bottom_tape = Polygon.make_polygon(bottom_tape, frame, mask)

# top_tape.run(contours)
# bottom_tape.run(contours)

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
# lower_green = np.array([50, 250, 30])
# upper_green = np.array([65, 255, 60])

# BGR
lower_green = np.array([Constants.low_blue, Constants.low_green, Constants.low_red])
upper_green = np.array([Constants.upper_blue, Constants.upper_green, Constants.upper_red])

distance = 0
# Starts video capture
# Creates two video windows. One from camera feed. Other blacks out everything not between calibrated BGR ranges

while (True):
    ret, frame = vid.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    '''
    # contours:
    im2, contours, hierarchy = cv2.findContours(mask, 2, 1)  # without 'im2' for opencv2.4 !!
    if len(contours) > 0:
        cnt = contours[0]
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)
    '''

    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    print 'Contour count is ' + str(len(contours))
    for c in contours:

        # find minimum area
        rect = cv2.minAreaRect(c)
        # calculate coordinates of the minimum area rectangle
        box = cv2.boxPoints(rect)
        # normalize coordinates to integers
        box = np.int0(box)
        # draw contours
        # cv2.drawContours(frame, [box], 0, (0, 0, 255), 3)
        # calculate center and radius of minimum enclosing circle
        (x, y), radius = cv2.minEnclosingCircle(c)

        # cast to integers
        center = (int(x), int(y))
        radius = int(radius)
        # draw the circle
        # print center
        # print 'meters are: ' + str(meters)
        epsilon = 0.000001 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)

        print 'Approx is ' + str(len(approx))
        if len(approx) > 4:
            tape_contour.append(approx)

        if (len(tape_contour) > 0 and len(tape_contour) < 4):
            for x in range(0, len(tape_contour)):
                cv2.drawContours(frame, tape_contour, -1, (0, 0, 255), 2)
                cv2.circle(frame, center, radius, (0, 255, 0), 2)

        # print len(tape_contour)

        try:
            socket.put("centerX", str(center))
        except Exception as e:
            print "Can't connect : {0}".format(e)

    cv2.imshow('orig', frame)
    # cv2.imshow('mask', mask)
    # cv2.imshow('res', res)
    #cv2.imshow("hsv", hsv)
    tape_contour = []
    k = cv2.waitKey(20) & 0xFF
    if k == ord('q'):
        break

# exits
vid.release()
cv2.destroyAllWindows()