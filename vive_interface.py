
#!/usr/bin/env python

import rospy
import sys
import actionlib
from std_msgs.msg import Int32
from std_msgs.msg import Float32
from geometry_msgs.msg import PoseStamped
from control_msgs.msg import (
    GripperCommandAction,
    GripperCommandGoal,
)

global cmd_label
global command_publisher
cmd_label = 0

def main():
	rospy.Subscriber("controller_pose", PoseStamped, command_callback, queue_size=1)

	#these 3 lines attempt to maintain the loop at 500 hz
	r = rospy.Rate(500)
	while not rospy.is_shutdown():
		r.sleep()


def command_callback(msg):
    global command_publisher
    global cmd_label
    if cmd_label == 1:
        command_publisher.publish(msg)

    print(msg.Pose.Point.x)


