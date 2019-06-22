#!/usr/bin/env python3

# A basic example of using BlueInterface for joint positions control.
# It allows a user to record four sets of joint positions by manually moving the arm to each
# position and pressing enter. It then plays back a trajectory comprised of the four sets of
# joint positions in an infinite loop.

import sys
from blue_interface import BlueInterface
import numpy as np
import time

side = "right"
ip = "127.0.0.1"
blue = BlueInterface(side, ip)

print_aligned = lambda left, right: print("{:30} {}".format(left, np.round(right, 4)))
while True:
    print_aligned("End Effector Position:", blue.get_cartesian_pose()['position'])
    print_aligned("End Effector Orientation:", blue.get_cartesian_pose()['orientation'])
    print_aligned("Joint Positions:", blue.get_joint_positions())
    print_aligned("Joint Velocities:", blue.get_joint_velocities())
    print_aligned("Joint Torques:", blue.get_joint_torques())
    print_aligned("Gripper Position:", blue.get_gripper_position())
    print_aligned("Gripper Effort:", blue.get_gripper_effort())
    print("=" * 30)
    time.sleep(0.5)

