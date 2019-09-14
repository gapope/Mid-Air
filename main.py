import sys

sys.path.append('PATH/lib')

import Leap, thread, time

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

from leapListener import *

def main():
    # Create a sample listener and controller
    listener = LeapListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener) 

if __name__ == "__main__":
    main()