import cv2


class Polygon:
    tape_contour = []
    mask = None
    frame = None
    width = 0
    length = 0
    ratio = 0
    center = None

    def __init__(self, frame, mask):
        self.mask = mask
        self.frame = frame

    def make_polygon(self, frame, mask):
        polygon = Polygon(frame, mask)
        return polygon


    def run(self):

        # global contours, tape_contour, frame, mask
        im2, contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            (x, y), radius = cv2.minEnclosingCircle(c)

            # cast to integers
            center = (int(x), int(y))
            radius = int(radius)

            # draw the circle
            # print center
            # print 'meters are: ' + str(meters)
            epsilon = 0.000001 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)

            if len(approx) > 4:
                self.tape_contour.append(approx)

            if (len(self.tape_contour) > 0 and len(self.tape_contour) < 2):
                for x in range(0, len(self.tape_contour)):
                    cv2.drawContours(self.frame, self.tape_contour, 0, (0, 0, 255), 2)
                    cv2.circle(self.frame, center, radius, (0, 255, 0), 2)
