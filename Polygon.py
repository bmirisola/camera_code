import cv2

class Polygon:
    tape_contour = []
    mask = None
    frame = None
    width = 0
    length = 0
    ratio = 0
    center = []
    temp = None

    def __init__(self, frame, mask):
        self.mask = mask
        self.frame = frame
        self.tape_contour = []

    def __getitem__(self, item):
        return item

    def run(self, contours):

        # calculate center and radius of minimum enclosing circle
        (x, y), radius = cv2.minEnclosingCircle(contours)

        # cast to integers
        self.center = (int(x), int(y))
        radius = int(radius)
        # draw the circle
        # print center
        # print 'meters are: ' + str(meters)
        epsilon = 0.000001 * cv2.arcLength(contours, True)
        approx = cv2.approxPolyDP(contours, epsilon, True)

        if len(approx) > 4:
            self.tape_contour.append(approx)

        if (len(self.tape_contour) > 0 and len(self.tape_contour) < 2):
            for x in range(0, len(self.tape_contour)):
                cv2.drawContours(self.frame, self.tape_contour, 0, (0, 0, 255), 2)
                cv2.circle(self.frame, self.center, radius, (0, 255, 0), 2)

        center = list(self.center)
        self.tape_contour = []