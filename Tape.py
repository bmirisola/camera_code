import cv2
import numpy as np

# Creates video capture object from camera
vid = cv2.VideoCapture(1)

# X and Y coordinates of mouseclick
coX, coY = 0, 0

# pixel array that will hold BGR values of the pixel at X and Y
px = []


# detects double left click and stores the coordinates in px
# This is for calibrating pixel values of retro tape so that everything can be blocked out
def printpix(event, x, y, flags, params):
    global coX, coY, px
    if event == cv2.EVENT_LBUTTONDBLCLK:
        coX, coY = x, y
        px = frame[coY, coX]


# Sets printpix function frame titled 'orig'
cv2.namedWindow('orig')
cv2.setMouseCallback('orig', printpix)

# Calibrated pixel ranges
lower_green = np.array([5, 10, 20])
upper_green = np.array([100, 75, 40])

# Starts video capture
# Creates two video windows. One from camera feed. Other blacks out everything not between calibrated BGR ranges

while (True):
    ret, frame = vid.read()
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv, lower_green, upper_green)
    # res = cv2.bitwise_and(frame,frame,mask=mask)
    cv2.imshow('orig', frame)
    # cv2.imshow('fff',res)

    # if 'a' key is pressed BGR values are printed. If 'q' is pressed while loop breaks
    k = cv2.waitKey(20) & 0xFF
    if k == ord('q'):
        break

    elif k == ord('a'):
        print px

# exits
vid.release()
cv2.destroyAllWindows()
