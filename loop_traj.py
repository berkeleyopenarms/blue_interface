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

MODE = "RECORD"
# MODE = "PLAY"

filename = "loop_test_data.pickle"

def cheb_points(n, k):
    xk = np.cos( (2.0 * k  - 1.0) / (2.0 * n) * np.pi )
    return (-xk + 1.0) / 2.0

num_points = int(sys.argv[1])
# resolution = int(sys.argv[2])
resolution = 100
duration = 2
end_pause = 3

blue = BlueInterface("right", "hekate.cs.berkeley.edu")
recorded_positions = []
error = 0.2

blue.disable_control()
blue.disable_gripper()

if MODE == "RECORD":
    if len(sys.argv) != 2:
        print("give me number of points")
        exit()

    #TODO: make number of positions a command line arg
    for _ in range(num_points):
        raw_input("Press enter to record current joint positions.")
        recorded_positions.append(blue.get_joint_positions())

    # with open('tape_trajectory.pickle', 'wb') as handle:
    #     pickle.dump(recorded_positions, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #
    traj = []
    for start_pos, end_pos in zip(recorded_positions[:-1], recorded_positions[1:]):
        for i in range(resolution + 1):
            step = start_pos + (end_pos - start_pos) * cheb_points(resolution, i)
            traj.append(step)

    data = traj
    with open(filename, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # traj_rev = traj[::-1]
    # traj.extend(traj_rev)


elif MODE == "PLAY":

    with open(filename, 'rb') as handle:
        traj = pickle.load(handle);

    print(traj)
    raw_input("Press enter to start trajectory.")

    print(recorded_positions[0])
    print(recorded_positions[-1])
    with open('start_end_joints.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(recorded_positions[0])
        writer.writerow(recorded_positions[-1])

    while True:
        for desired_position in traj:
            current_position = blue.get_joint_positions()
            blue.set_joint_positions(np.array(desired_position))
            # blue.command_gripper(desired_position[0], 2.0, True)

            time.sleep(duration * 1.0 / resolution)
            # while np.linalg.norm(desired_position - current_position) > error:
            #     current_position = blue.get_joint_positions()
            #     time.sleep(0.1)
        time.sleep( end_pause )
        for desired_position in traj[::-1]:
            current_position = blue.get_joint_positions()
            blue.set_joint_positions(np.array(desired_position))
            # blue.command_gripper(desired_position[0], 2.0, True)

            time.sleep(duration * 1.0 / resolution)
        time.sleep( end_pause )


blue.cleanup()
