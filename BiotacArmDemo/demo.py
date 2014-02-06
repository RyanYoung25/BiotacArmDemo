#!/usr/bin/env python
'''
This node is run in conjunction with the biotac_sensors exceutable. It will
get the pressure from the biotac sensor and correlate it with elbow joint commands
on hubo.

Author: Ryan
'''

import roslib; roslib.load_manifest('BiotacArmDemo')
import rospy
import time
import sys
from hubomsg.msg import *
from biotac_sensors.msg import *

ID_NUM = 7
'''
This is a demo class. It basically when created will handle
the demo. Every time it gets a biotac_pub message it goes through
the call back. 
'''
class demo:

    def __init__(self):
        self.INCREMENT = .05
        self.MAX = 1
        rospy.init_node("BioTacDemo")
        rospy.Subscriber("biotac_pub", BioTacHand, self.update)
        self.pub = rospy.Publisher("Maestro/Control", MaestroCommand)
        self.count = 0
        rospy.on_shutdown(self.exit)
        rospy.spin()
    
    '''
    The heart of the demo 
    '''
    def update(self, handData):
        data = handData.bt_data
        pressure = data[0].pdc_data
        pos = (pressure - 2000) / 150.0  #Scale it!
        if pos > 1.6:
            pos = 1.6
        elif pos < 0:
            pos = 0         
        print "pos: " + str(pos)
        pos = -pos  #elbow likes negative values for position
        #This is so that the increments happens and the maestro topic is not overrun 
        self.count += 1                         
        if self.count == 10: 
            self.count = 0
            self.pub.publish("REP", "position", str(pos), "", ID_NUM)

    def exit(self):
        self.pub.publish("REP", "position", "0", "", ID_NUM)
        


    
if __name__ == '__main__':
    print "Starting the biotac elbow demo"
    demo = demo()
    
