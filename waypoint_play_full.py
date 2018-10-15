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

blue_r = BlueInterface("right", "localhost")
recorded_positions_r = []
recorded_grippers_r  = []
blue_r.disable_control()
blue_r.disable_gripper()



blue_l = BlueInterface("left", "localhost")
recorded_positions_l = []
recorded_grippers_l  = []
blue_l.disable_control()
blue_l.disable_gripper()

joints_r = []
grippers_r = []
joints_l = []
grippers_l = []
with open(filename, 'rb') as handle:
    joints_r, grippers_r, joints_l, grippers_l = pickle.load(handle);
    joints_r =np.array(joints_r)
    joints_l =np.array(joints_l)


start_jp_r = []
start_jp_l = []
while (True):
    start_jp_r = blue_r.get_joint_positions()
    start_jp_l = blue_l.get_joint_positions()
    if start_jp_r.size == 7 and start_jp_l.size == 7:
        break
    print("failed, trying again")
print(start_jp_r)
print(start_jp_l)

print("READY\n\n")
for j in range(resolution + 1):
    step = start_jp_r + (joints_r[0] - start_jp_r) * cheb_points(resolution, j)
    blue_r.set_joint_positions(np.array(step))

    step = start_jp_l + (joints_l[0] - start_jp_l) * cheb_points(resolution, j)
    blue_l.set_joint_positions(np.array(step))

    time.sleep(duration * 1.0 / resolution)

grip_mode_r = grip(blue_r, grippers_r[0])
grip_mode_l = grip(blue_l, grippers_l[0])

for i in range( len(joints_r) - 1):
    start_pos_r = joints_r[i]
    end_pos_r = joints_r[i+1]

    start_pos_l = joints_l[i]
    end_pos_l = joints_l[i+1]

    joint_diff_r = end_pos_r - start_pos_r
    max_joint_diff_r = np.linalg.norm(joint_diff_r, np.inf)
    joint_diff_l = end_pos_l - start_pos_l
    max_joint_diff_l = np.linalg.norm(joint_diff_l, np.inf)

    max_joint_diff = max(max_joint_diff_l, max_joint_diff_r)


    for j in range(resolution + 1):
        step = start_pos_r + (end_pos_r - start_pos_r) * cheb_points(resolution, j)
        blue_r.set_joint_positions(np.array(step))

        step = start_pos_l + (end_pos_l - start_pos_l) * cheb_points(resolution, j)
        blue_l.set_joint_positions(np.array(step))

        time.sleep( np.abs(max_joint_diff) * duration * 1.0 / resolution)

    wait_duration = 0.0;
    old_grip_r = grip_mode_r
    grip_mode_r = grip(blue_r, grippers_r[i+1])
    if not grip_mode_r == old_grip_r:
        wait_duration = 1.0

    old_grip_l = grip_mode_l
    grip_mode_l = grip(blue_l, grippers_l[i+1])
    if not grip_mode_l == old_grip_l:
        wait_duration = 1.0

    time.sleep(wait_duration)

blue_r.cleanup()
blue_l.cleanup()
