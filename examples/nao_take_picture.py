# -*- encoding: UTF-8 -*-

''' PoseZero: Set all the motors of the body to zero. '''

import argparse
import os
import sys
import time
from naoqi import ALProxy
import vision_definitions

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
    camID = videoDeviceProxy.subscribe(subscriberID, vision_definitions.kVGA, vision_definitions.kRGBColorSpace, fps);

    image = videoDeviceProxy.getImageRemote(camID)

    # print image
    image_file = open('image.yuv', 'w')
    image_file.write(bytes(image))
    
    # Unsubscribe the V.M.
    videoDeviceProxy.unsubscribe(camID);

    '''
    videoDeviceProxy.setResolution(2)
    videoDeviceProxy.setPictureFormat("jpg")
    videoDeviceProxy.takePicture("/home/idhuser/", "image")
    '''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
