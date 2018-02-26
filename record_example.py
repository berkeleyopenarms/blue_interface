#!/usr/bin/env python3
from koko_interface import KokoInterface
import numpy as np
import time

# records and plays back a trajectory comprised of 4 joint positions

koko = KokoInterface('hekate.cs.berkeley.edu')
koko.disable_control()
recorded_positions = []
error = 0.5

for _ in range(4):
    input("Press enter to continue...")
    recorded_positions.append(koko.get_joint_positions())

input("Press enter to start trajectory.")
koko.enable_control()

while True:
    for des_pos in recorded_positions:
        curr_pos = koko.get_joint_positions()
        while (np.linalg.norm(np.subtract(des_pos, curr_pos)) > error):
