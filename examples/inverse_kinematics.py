#!/usr/bin/env python3

# A basic example of sending Blue a command in cartesian space.

import time

import numpy as np

from blue_interface import BlueInterface

side = "right"
ip = "127.0.0.1"
blue = BlueInterface(side, ip)

# Compute IK solution
target_position = [0.4, 0, 0]  # x, y, z
target_orientation = [0.6847088, -0.17378805, -0.69229771, -0.1472938]  # x, y, z, w
target_joint_positions = blue.inverse_kinematics(target_position, target_orientation)

# Send command to robot
blue.set_joint_positions(target_joint_positions, duration=5)

# Wait for system to settle
time.sleep(5)

# Print results
joint_positions = blue.get_joint_positions()
pose = blue.get_cartesian_pose()
print_aligned = lambda left, right: print("{:30} {}".format(left, np.round(right, 4)))
print_aligned("Target joint positions: ", target_joint_positions)
print_aligned("End joint positions: ", joint_positions)
print_aligned("Target cartesian position:", target_position)
print_aligned("End cartesian position:", pose["position"])
print_aligned("Target orientation:", target_orientation)
print_aligned("End orientation:", pose["orientation"])
