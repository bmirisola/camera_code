import cv2

class Polygon:
    # parameters for contours and polygons
    tape_contour = []
    mask = None
    frame = None
    radius = 0
    center = []

    #Contstructor to make Polygon objects
    def __init__(self, frame, mask):
        self.mask = mask
        self.frame = frame
        self.tape_contour = []

    #Draws contours
    def run(self, contours):

        # calculate center and radius of minimum enclosing circle
        (x, y), radius = cv2.minEnclosingCircle(contours)

        # cast to integers
        self.center = (int(x), int(y))
        self.radius = int(radius)

        #Creates Polygon on a 0.001% error to contours
        epsilon = 0.000001 * cv2.arcLength(contours, True)
        approx = cv2.approxPolyDP(contours, epsilon, True)

        #Add Polygons to tape contour if they are of point size 4 or greater
        if len(approx) > 2:
            self.tape_contour.append(approx)

        #draw all detected polygons
        if (len(self.tape_contour) > 0 and len(self.tape_contour) < 2):
            for x in range(0, len(self.tape_contour)):
                cv2.drawContours(self.frame, self.tape_contour, 0, (0, 0, 255), 2)
                cv2.circle(self.frame, self.center, self.radius, (0, 255, 0), 2)

        #converts center to list from tuple
        self.center = list(self.center)

        #Clears polygons from tape contour array
        self.tape_contour = []