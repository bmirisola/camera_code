# 11 3/8 inches 11.375 inches
def find_focal_length(distance, width,pixel):
    return (pixel * distance) / width


# focal length = 607.648351648

def find_distance(focal_length, width, pixel):
    if pixel != 0:
        return (focal_length * width) / pixel
    else:
        return 1
