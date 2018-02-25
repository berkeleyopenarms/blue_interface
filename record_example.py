#!/usr/bin/env python3
from koko_interface import KokoInterface
import numpy as np
import time

if __name__== '__main__':

    koko = KokoInterface('hekate.cs.berkeley.edu')
    count = 0
    recorded_positions = []
    koko.pd_off()
    while count < 4:
        input("Press enter to continue...")
        print("pressed enter")
        koko.get_joint_angles()
        print("got_joint_angles")
        recorded_positions.append(koko.get_joint_angles())
        count+=1
    print(recorded_positions)
    input("Press enter to start trajectory")
    koko.pd_on()
    while True:
        for des_pos in recorded_positions:
            print("New Joint Position")
            error = 0.23
            curr_pos = koko.get_joint_angles()
            while (np.linalg.norm(np.subtract(des_pos, curr_pos)) > error):
                koko.set_joint_angle_target(des_pos)
                curr_pos = koko.get_joint_angles()


