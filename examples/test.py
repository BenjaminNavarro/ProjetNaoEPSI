# -*- encoding: UTF-8 -*-

''' PoseZero: Set all the motors of the body to zero. '''

import argparse
from naoqi import ALProxy

def main(robotIP, PORT=9559):

    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    # Wake up robot
    motionProxy.wakeUp()

    # Send robot to Stand Zero
    #postureProxy.goToPosture("StandZero", 0.5)

    #id = motionProxy.post.openHand("LHand")
    #motionProxy.wait( id, 0 )

    # Go to rest position
    #motionProxy.rest()

    postureProxy.goToPosture("StandInit", 0.5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)
