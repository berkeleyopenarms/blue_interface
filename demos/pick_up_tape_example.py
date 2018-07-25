#!/usr/bin/env python3

# A basic example of using BlueInterface for joint positions control.
# It allows a user to record four sets of joint positions by manually moving the arm to each
# position and pressing enter. It then plays back a trajectory comprised of the four sets of
# joint positions in an infinite loop.

import sys
sys.path.append('../')
from blue_interface import BlueInterface
import numpy as np
import time
import pickle
import consts

blue = BlueInterface(consts.default_arm, consts.default_address)
print("..")
recorded_positions = []
error = 0.5

blue.disable_control()
blue.disable_gripper()

#TODO: make number of positions a command line arg
with open('tape_trajectory.pickle', 'rb') as handle:
    recorded_positions = pickle.load(handle)

input("Press enter to start trajectory.")

while True:
    for desired_position in recorded_positions:
        current_position = (blue.get_gripper_position(), blue.get_joint_positions())
        blue.set_joint_positions(np.array(desired_position[1]))
        blue.command_gripper(desired_position[0], 2.0, True)
        while np.linalg.norm(desired_position[1] - current_position[1]) > error:
            current_position = (blue.get_gripper_position(), blue.get_joint_positions())
            time.sleep(0.1)
