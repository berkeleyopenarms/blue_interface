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
if len(sys.argv) == 2:
    filename = sys.argv[1]
elif len(sys.argv) == 1:
    filename = "waypoint_data.pickle"
else:
    print("give me nothing ")
    print("or give me a pickle file nothing ")
    exit()

resolution = 100
duration = 2

def cheb_points(n, k):
    # return float(k)/float(n)
    xk = np.cos( (2.0 * k  - 1.0) / (2.0 * n) * np.pi )
    return (-xk + 1.0) / 2.0

def grip(blue, x):
    if x < -0.2:
        blue.command_gripper(-1.2, 18.0, wait=False)
        # blue.command_gripper(-1.2, 18.0, wait=True)
        return True
    else:
        blue.command_gripper(0.1, 4.0, wait=False)
        # blue.command_gripper(0.1, 4.0, wait=True)
        return False


blue = BlueInterface("right", "localhost")
recorded_positions = []
recorded_grippers  = []

blue.disable_control()
blue.disable_gripper()

joints = []
grippers = []
with open(filename, 'rb') as handle:
    joints, grippers = pickle.load(handle);
    joints =np.array(joints)


print(joints[0])
print(len(joints))
print(grippers)
raw_input("Press enter to move to star position.")

start_jp = []
while (True):
    start_jp = blue.get_joint_positions()
    if start_jp.size == 7:
        break
    print("failed, trying again")

for j in range(resolution + 1):
    step = start_jp + (joints[0] - start_jp) * cheb_points(resolution, j)
    blue.set_joint_positions(np.array(step))
    time.sleep(duration * 1.0 / resolution)

grip_mode = grip(blue, grippers[0])

raw_input("Press enter to start trajectory.")

for i in range( len(joints)- 1):
    start_pos = joints[i]
    end_pos = joints[i+1]

    joint_diff = end_pos - start_pos
    max_joint_diff = np.linalg.norm(joint_diff, np.inf)
    print(max_joint_diff)

    for j in range(resolution + 1):
        step = start_pos + (end_pos - start_pos) * cheb_points(resolution, j)
        blue.set_joint_positions(np.array(step))
        time.sleep( np.abs(max_joint_diff) * duration * 1.0 / resolution)

    old_grip = grip_mode
    grip_mode = grip(blue, grippers[i+1])
    if not grip_mode == old_grip:
        time.sleep(1.0)
        print("done gripping")

blue.cleanup()
