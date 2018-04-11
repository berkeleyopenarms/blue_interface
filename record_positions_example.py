#!/usr/bin/env python3

# A basic example of using KokoInterface for joint positions control.
# It allows a user to record four sets of joint positions by manually moving the arm to each
# position and pressing enter. It then plays back a trajectory comprised of the four sets of
# joint positions in an infinite loop.

from koko_interface import KokoInterface
import numpy as np
import time

koko = KokoInterface("hekate.cs.berkeley.edu")
print("made a Koko object")
recorded_positions = []
error = 0.1

koko.disable_control()
koko.disable_gripper()

#TODO: make number of positions a command line arg
for _ in range(10):
    input("Press enter to record current joint positions.")
    recorded_positions.append((koko.get_gripper_position(), koko.get_joint_positions()))
input("Press enter to start trajectory.")

while True:
    for desired_position in recorded_positions:
        current_position = (koko.get_gripper_position(), koko.get_joint_positions())
        koko.set_joint_positions(np.array(desired_position[1]))
        koko.command_gripper(desired_position[0], 2.0, True)
        while np.linalg.norm(desired_position[1] - current_position[1]) > error:
            current_position = (koko.get_gripper_position(), koko.get_joint_positions())
            time.sleep(0.1)
