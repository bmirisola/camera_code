# 11 3/8 inches 11.375 inches
def focal_length(pixel, width, distance):
    return (pixel * distance) / width


# focal length = 607.648351648


def find_distance(focal_length, width, pixel):
    return (focal_length * width) / pixel
