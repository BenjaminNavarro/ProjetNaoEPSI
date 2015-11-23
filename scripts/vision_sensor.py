# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:30:54 2015

@author: Pierre Jacquot
"""

import vrep,time,sys
import matplotlib.pyplot as plt
from PIL import Image as I
import array
from naoqi import ALProxy
import vision_definitions
from io import BytesIO
import numpy as np

videoDeviceProxy = ALProxy

def streamVisionSensor(visionSensorName,clientID,pause,sample_time):
    #Get the handle of the vision sensor
    res1,visionSensorHandle=vrep.simxGetObjectHandle(clientID,visionSensorName,vrep.simx_opmode_oneshot_wait)
    #Get the image
    res2,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_streaming)
    #Allow the display to be refreshed
    plt.ion()
    #Initialiazation of the figure
    time.sleep(0.5)
    res,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_buffer)
    print resolution
    im = I.new("RGB", (resolution[0], resolution[1]), "white")
    #Give a title to the figure
    fig = plt.figure(1)    
    fig.canvas.set_window_title(visionSensorName)
    #inverse the picture
    plotimg = plt.imshow(im,origin='lower')
    #Let some time to Vrep in order to let him send the first image, otherwise the loop will start with an empty image and will crash
    time.sleep(1)
    img = I.new("RGB", (resolution[0], resolution[1]))
    while (vrep.simxGetConnectionId(clientID)!=-1): 
        start = time.time()
        #Get the image of the vision sensor
        res,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_buffer)
        #Transform the image so it can be displayed using pyplot
        image_byte_array = array.array('b',image)
        im = I.frombuffer("RGB", (resolution[0],resolution[1]), image_byte_array, "raw", "RGB", 0, 1)
        #Update the image
        plotimg.set_data(im)
        #Refresh the display
        plt.draw()
        #The mandatory pause ! (or it'll not work)
        plt.pause(pause)
        #Set the image for naoqi
        imagepixel = []#*(resolution[0]*resolution[1])
        for i in xrange(resolution[0] * resolution[1]):
            r = i*3
            g = r+1
            b = r+2
            imagepixel.append((image[b], image[g], image[r]))
        img.putdata(imagepixel)
        # print image
        # print imagepixel
        data = img.tostring()
        im = im.rotate(180)
        videoDeviceProxy.putImage(vision_definitions.kTopCamera, resolution[0], resolution[1], im.tostring())
        end = time.time()
        dt = end-start
        if dt < sample_time:
            time.sleep(sample_time - dt)
        else:
            print "Can't keep a period (%gs>%gs)" % (dt,sample_time)

    print 'End of Simulation'
    
def getVisionSensor(visionSensorName,clientID,sample_time):
    #Get the handle of the vision sensor
    res1,visionSensorHandle=vrep.simxGetObjectHandle(clientID,visionSensorName,vrep.simx_opmode_oneshot_wait)
    #Get the image
    res2,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_streaming)
    time.sleep(0.5)
    res2,resolution,image=vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_buffer)
    print resolution
    img = I.new("RGB", (resolution[0], resolution[1]))
    while (vrep.simxGetConnectionId(clientID)!=-1): 
        start = time.time()
        #Get the image of the vision sensor
        res,resolution,image = vrep.simxGetVisionSensorImage(clientID,visionSensorHandle,0,vrep.simx_opmode_buffer)

        image_byte_array = array.array('b',image)
        im = I.frombuffer("RGB", (resolution[0],resolution[1]), image_byte_array, "raw", "RGB", 0, 1)

        # #Set the image for naoqi
        # imagepixel = []#*(resolution[0]*resolution[1])
        # for i in xrange(resolution[0] * resolution[1]):
        #     r = i*3
        #     g = r+1
        #     b = r+2
        #     imagepixel.append((image[b], image[g], image[r]))
        # img.putdata(imagepixel)
        # print image
        # print imagepixel
        videoDeviceProxy.putImage(vision_definitions.kTopCamera, resolution[0], resolution[1], im.rotate(180).tostring())
        end = time.time()
        dt = end-start
        # if dt < sample_time:
        #     time.sleep(sample_time - dt)
        # else:
        #     print "Can't keep a period (%gs>%gs)" % (dt,sample_time)
    print 'End of Simulation'
    
if __name__ == '__main__':
    #vrep.simxFinish(-1)
    sample_time = 0.2
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
    global videoDeviceProxy
    if clientID!=-1:
        print 'Connected to remote API server'
        # Create a proxy to ALVideoDevice
        try:
            videoDeviceProxy = ALProxy('ALVideoDevice', '127.0.0.1', 9559)
        except Exception, e:
            print "Error when creating ALVideoDevice proxy:"
            print str(e)
            exit(1)

        # Subscribe a Vision Module to ALVideoDevice, starting the
        # frame grabber if it was not started before.
        subscriberID = 'vrep_bridge'
        fps = 5
        # The subscriberID can be altered if other instances are already running
        camID = videoDeviceProxy.subscribe(subscriberID, vision_definitions.kVGA, vision_definitions.kRGBColorSpace, fps);


        #Get and display the pictures from the camera
        #streamVisionSensor('NAO_vision1',clientID,0.0001,sample_time)
        #Only get the image
        getVisionSensor('NAO_vision1',clientID, sample_time)

        # Unsubscribe the V.M.
        videoDeviceProxy.unsubscribe(camID);

    else:
        print 'Connection non successful'
        sys.exit('Could not connect')
