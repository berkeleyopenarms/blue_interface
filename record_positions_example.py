#!/usr/bin/env python3
from koko_interface import KokoInterface
import numpy as np
import time

"""A Hello World for using KokoInterface for joint positions control.

Records four sets of joint positions by manually moving the arm to each position and pressing enter. Plays back a trajectory comprised of the four sets of joint positions on an infinite loop.
"""

koko = KokoInterface("hekate.cs.berkeley.edu")
koko.disable_control()
recorded_positions = []
error = 0.5

for _ in range(4):
    input("Press enter to record current joint positions.")
    recorded_positions = np.append(recorded_positions, koko.get_joint_positions())

input("Press enter to start trajectory.")

while True:
    for des_pos in recorded_positions:
        curr_pos = koko.get_joint_positions()
        while (np.linalg.norm(des_pos - curr_pos) > error):
            koko.set_joint_positions(des_pos)
            curr_pos = koko.get_joint_positions()
