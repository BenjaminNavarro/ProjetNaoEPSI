# -*- encoding: UTF-8 -*-

''' PoseZero: Set all the motors of the body to zero. '''

import argparse
import os
import sys
import time
from naoqi import ALProxy
import vision_definitions
import cv2
import numpy as np

def main(robotIP, PORT=9559):
    # Create a proxy to ALPhotoCapture
    try:
        videoDeviceProxy = ALProxy("ALVideoDevice", robotIP, PORT)
    except Exception, e:
        print "Error when creating ALVideoDevice proxy:"
        print str(e)
        exit(1)

    # Subscribe a Vision Module to ALVideoDevice, starting the
    # frame grabber if it was not started before.
    subscriberID = 'subscriberID'
    fps = 5
    # The subscriberID can be altered if other instances are already running
    camID = videoDeviceProxy.subscribe(subscriberID, vision_definitions.kVGA, vision_definitions.kBGRColorSpace, fps);

    image = videoDeviceProxy.getImageRemote(camID)

    width = 640
    height = 480
    image_cv = np.zeros((height, width, 3), np.uint8)

    # translate value to mat
    values = map(ord, list(image[6]))
    i = 0
    for y in range(0, height):
        for x in range(0, width):
            image_cv.itemset((y, x, 0), values[i + 0])
            image_cv.itemset((y, x, 1), values[i + 1])
            image_cv.itemset((y, x, 2), values[i + 2])
            i += 3

    # show image
    cv2.imshow("nao image", image_cv)

    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    cv2.imshow("nao image gray", gray)

    cv2.waitKey()

    # Unsubscribe the V.M.
    videoDeviceProxy.unsubscribe(camID);

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
