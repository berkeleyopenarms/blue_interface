#!/usr/bin/env python3
from koko_interface import KokoInterface, KokoControlMode
import numpy as np
import time

"""A Hello World for using KokoInterface for cartesian pose control.

Records four cartesian poses by manually moving the arm to each pose and pressing enter. Plays back trajectory comprised of the four poses on an infinite loop.
"""

koko = KokoInterface("hekate.cs.berkeley.edu")
koko.set_control_mode(KokoControlMode.CONTROL_OFF)
recorded_poses = []
pos_error = 0.05
orient_error = 0.5

for _ in range(4):
    input("Press enter to record current pose.")
    recorded_poses = np.append(recorded_poses, koko.get_cartesian_pose())

input("Press enter to start the trajectory!")
koko.set_control_mode(KokoControlMode.CARTESIAN_POSE)

while True:
    for des_pose in recorded_poses:
        curr_pose = koko.get_cartesian_pose()
        curr_pos = curr_pose["position"]
        curr_orientation = curr_pose["orientation"]
        des_pos = des_pose["position"]
        des_orient = des_pose["orientation"]
        while ((np.linalg.norm(des_pos - curr_pos) > pos_error) or (np.linalg.norm(des_orient - curr_orient) > orient_error)):
            koko.set_cartesian_pose(des_pose)
            curr_pose = koko.get_cartesian_pose()
            curr_pos = curr_pose["position"]
            curr_orientation = curr_pose["orientation"]
