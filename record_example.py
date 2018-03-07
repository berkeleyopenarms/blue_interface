#!/usr/bin/env python3
from koko_interface import KokoInterface, KokoControlMode
import numpy as np
import time

# records and plays back a trajectory comprised of 4 joint positions

koko = KokoInterface("hekate.cs.berkeley.edu")
koko.set_control_mode(KokoControlMode.CONTROL_OFF)
recorded_positions = []
error = 0.5

for _ in range(4):
    input("Press enter to continue...")
    np.append(recorded_positions, koko.get_joint_positions())
    recorded_positions.append(koko.get_joint_positions())

input("Press enter to start trajectory.")
koko.set_control_mode(KokoControlMode.JOINT_POSITIONS)

while True:
    for des_pos in recorded_positions:
        curr_pos = koko.get_joint_positions()
        while (np.linalg.norm(des_pos - curr_pos) > error):
            koko.set_joint_positions(des_pos)
            curr_pos = koko.get_joint_positions()
