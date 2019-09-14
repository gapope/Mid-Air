import sys

sys.path.append('/Users/Greg/Leap/lib')

import Leap, thread, time

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

from leapListener import *

def main():
    # Create a sample listener and controller
    listener = LeapListener()
    controller = Leap.Controller()

    waiting = True
    line = ''

    while 'x' not in line:

        # Keep this process running until Enter is pressed
        print "Press Enter to start/stop, x to quit..."
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            pass
        finally:
            if waiting:
                listener.pointList = []
                
                # Have the sample listener receive events from the controller
                controller.add_listener(listener)
            else:
                # Remove the sample listener when done
                controller.remove_listener(listener) 

                print str(listener.pointList)

            waiting = not waiting

if __name__ == "__main__":
    main()