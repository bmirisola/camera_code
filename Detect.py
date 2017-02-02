import numpy as np
import os
import time

import cv2

import Constants
import Distance
from UDPCannon import UDPCannon

vid = cv2.VideoCapture(Constants.camera_port)
time.sleep(1)

os.system("scripts/configure.sh")

socket = UDPCannon("10.0.11.67", 8090)
tape_contour = []

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
lower_green = np.array([50, 250, 30])
upper_green = np.array([65, 255, 60])

# BGR
# lower_green = np.array([Constants.low_blue, Constants.low_green, Constants.low_red])
# upper_green = np.array([Constants.upper_blue, Constants.upper_green, Constants.upper_red])

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

    im2, contours, hierarchy = cv2.findContours(mask, 2, 1)
    for c in contours:
        # find minimum area
        rect = cv2.minAreaRect(c)
        # calculate coordinates of the minimum area rectangle
        box = cv2.boxPoints(rect)
        # normalize coordinates to integers
        box = np.int0(box)
        # draw contours
        #cv2.drawContours(frame, [box], 0, (0, 0, 255), 3)
        # calculate center and radius of minimum enclosing circle
        (x, y), radius = cv2.minEnclosingCircle(c)

        # cast to integers
        center = (int(x), int(y))
        radius = int(radius)
        distance = Distance.find_distance(Constants.focal_length, Constants.tape_width, radius * 2)
        meters = distance * 0.0254
        # draw the circle
        # print center
        # print 'meters are: ' + str(meters)
        cv2.circle(frame, center, radius, (0, 255, 0), 2)
        epsilon = 0.01 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        # print(len(c))
        if len(approx) >4:
            tape_contour.append(approx)

        if tape_contour:
            cv2.drawContours(frame, tape_contour, 0, (0, 0, 255), 1)
        try:
            socket.put("centerX", str(center))
            socket.put("distanceMeters", str(meters))
        except Exception as e:
            print "Can't connect : {0}".format(e)

    cv2.imshow('orig', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    cv2.imshow("hsv", hsv)
    k = cv2.waitKey(20) & 0xFF
    if k == ord('q'):
        break

# exits
vid.release()
cv2.destroyAllWindows()
