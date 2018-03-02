#!/usr/bin/env python

# Python 2/3 compatibility
import sys

PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range

import numpy as np
import cv2
import picamera
from time import sleep


def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))


def find_squares(img):
    #img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        _retval, bin = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        bin, contours, _hierarchy = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
            if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                cnt = cnt.reshape(-1, 2)
                max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                if max_cos < 0.1:
                    squares.append(cnt)
    return squares


def analyze_image():
    from glob import glob

    foo = glob('../data/pic*.png')
    for fn in glob('../data/pic*.png'):
        img = cv2.imread(fn)
        squares = find_squares(img)
        cv2.drawContours(img, squares, -1, (0, 255, 0), 3)
        cv2.imshow('squares', img)
        ch = cv2.waitKey()
        if ch == 27:
            break


if __name__ == '__main__':
    camera = picamera.PiCamera()
    camera.resolution = (1024,768)
    counter = 0
    while True:
        imageName = "pic_imageTest_" + str(counter) + ".jpg"

        camera.capture(imageName, resize=(320, 240))
        img = cv2.imread(imageName)
        
        listOfSquares = find_squares(img);
        if len(listOfSquares) == 0:
            print("No square found")
        else:
            print(str(len(listOfSquares)) + " Squares found!!")
            cv2.drawContours(img, listOfSquares, -1, (0, 255, 0), 3)
            cv2.imwrite("edited_" + imageName, img)
        
        counter = counter +1
        sleep(1)
        
#cv2.destroyAllWindows()