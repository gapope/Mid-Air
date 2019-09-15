'''
Modified version of the example listener from Leap
'''
import Leap

class LeapListener(Leap.Listener):
    pointLists = []
    writing = False

    def on_init(self, controller):
        print "Initialized"

    def reset_vals(self):
        self.pointLists = []
        self.writing = False

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        hand = None

        # Get hands
        for poss_hand in frame.hands:
            hand = poss_hand

            if hand.is_right:
                break
            
        if not frame.hands.is_empty:
            # Get fingers
            for finger in hand.fingers:
                if finger.type == finger.TYPE_INDEX:
                    #Find tip
                    joint = finger.bone(finger.JOINT_TIP).next_joint
                    
                    #Only use if in the 'writing range'
                    if joint.z > -50 and joint.z < 50:
                        #Start a new character if we aren't currently writing one
                        if not self.writing:
                            self.pointLists.append( ([], []) )
                            self.writing = True


                        print "("+ str(joint.x) +", "+ str(joint.y) +")"

                        #Record written points
                        self.pointLists[-1][0].append(joint.x)
                        self.pointLists[-1][1].append(joint.y)
                    #Mark character split
                    elif self.writing:
                        self.writing = False


        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"