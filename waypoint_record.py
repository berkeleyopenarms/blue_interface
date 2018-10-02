#!/usr/bin/env python3

# A basic example of using BlueInterface for joint positions control.
# It allows a user to record four sets of joint positions by manually moving the arm to each
# position and pressing enter. It then plays back a trajectory comprised of the four sets of
# joint positions in an infinite loop.

from blue_interface import BlueInterface
import numpy as np
import time
import pickle
import sys
import csv

filename = "waypoint_data.pickle"
num_points = 0

def cheb_points(n, k):
    xk = np.cos( (2.0 * k  - 1.0) / (2.0 * n) * np.pi )
    return (-xk + 1.0) / 2.0

if len(sys.argv) == 3:
    filename = sys.argv[1]
    num_points = int(sys.argv[2])
elif len(sys.argv) == 2:
    filename = "waypoint_data.pickle"
    num_points = int(sys.argv[1])
else:
    print("give me number of points")
    print("or give me a file name AND number of points")
    exit()


blue = BlueInterface("right", "localhost")
recorded_positions = []
recorded_grippers  = []

blue.disable_control()
blue.disable_gripper()


#TODO: make number of positions a command line arg
for _ in range(num_points):
    raw_input("Press enter to record current joint positions.")
    while (True):
        jp = blue.get_joint_positions()
        gp = blue.get_gripper_position()
        if jp.size == 7:
            print(jp)
            print(gp)
            recorded_positions.append(jp)
            recorded_grippers.append(gp)
            break
        print("failed, trying again")

with open(filename, 'wb') as handle:
    pickle.dump([recorded_positions, recorded_grippers], handle, protocol=pickle.HIGHEST_PROTOCOL)

blue.cleanup()
