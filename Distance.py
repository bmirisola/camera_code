import cv2
import numpy as np

def focal_length(image, width, distance):
    return (image * distance)/width

def distance(focalLength, width, image):
    return (focalLength* width)/ image