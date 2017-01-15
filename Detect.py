import cv2
import numpy as np
import os
import time
import Rectangle

#Creates video capture object from camera
vid = cv2.VideoCapture(1)
time.sleep(1)

os.system("/home/bennym/Desktop/turnonautoexposure.sh")
#os.system("/home/bennym/Desktop/turnoffautoexposure.sh")
os.system("/home/bennym/Desktop/all.sh")

#detects double left click and stores the coordinates in px
#This is for calibrating pixel values of retro tape so that everything can be blocked out
def printpix(event,x,y, flags, params):
    global hsv
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print hsv[y,x]

#Sets printpix function frame titled 'orig'
cv2.namedWindow('hsv')
cv2.setMouseCallback('hsv', printpix)


#Calibrated HSV Ranges
lower_green = np.array([0,0,230])
upper_green = np.array([255,255,255])

#Starts video capture
#Creates two video windows. One from camera feed. Other blacks out everything not between calibrated BGR ranges

while(True):
    ret, frame = vid.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(frame,frame,mask=mask)

    # contours:
    im2, contours, hierarchy = cv2.findContours(mask, 2, 1)  # without 'im2' for opencv2.4 !!
    if len(contours) > 0:
        cnt = contours[0]
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 4)

    cv2.imshow('orig',frame)
    cv2.imshow('fff',res)
    cv2.imshow("hsv", hsv)
    k = cv2.waitKey(20) & 0xFF
    if k == ord('q'):
        break

#exits
vid.release()
cv2.destroyAllWindows()
