#!/usr/bin/env python3

# A basic example of using KokoInterface for joint positions control.
# It allows a user to record four sets of joint positions by manually moving the arm to each
# position and pressing enter. It then plays back a trajectory comprised of the four sets of
# joint positions in an infinite loop.

from koko_interface import KokoInterface
import numpy as np

koko = KokoInterface("hekate.cs.berkeley.edu")
print("made a Koko object")
recorded_positions = []
error = 0.5

for _ in range(4):
    input("Press enter to record current joint positions.")
    recorded_positions.append(koko.get_joint_positions())
input("Press enter to start trajectory.")

while True:
    for desired_position in recorded_positions:
        current_position = koko.get_joint_positions()
        while np.linalg.norm(desired_position - current_position) > error:
            koko.set_joint_positions(np.array(desired_position))
            current_position = koko.get_joint_positions()
