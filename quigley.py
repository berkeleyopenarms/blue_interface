#!/usr/bin/env python3

# A basic example of using BlueInterface for joint positions control.
# It allows a user to record four sets of joint positions by manually moving the arm to each
# position and pressing enter. It then plays back a trajectory comprised of the four sets of
# joint positions in an infinite loop.

from blue_interface import BlueInterface
import numpy as np
import time
# import cPickle as pickle
import pickle
import sys
import csv

# MODE = "RECORD"
MODE = "PLAY"

filename = "quigley_test_data.pickle"

if len(sys.argv) != 2:
    print("give me number of points")
    exit()

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

    raw_input("Press enter to record Home.")
    home = blue.get_joint_positions()
    for _ in range(num_points):
        raw_input("Press enter to record current joint positions.")
        recorded_positions.append(blue.get_joint_positions())

    data = (recorded_positions, home)
    print(data)
    print(recorded_positions)
    print(home)
    with open('backup.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(filename, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

elif MODE == "PLAY":

    with open(filename, 'rb') as handle:
        (recorded_positions, home) = pickle.load(handle);

    raw_input("Press enter to start")

    with open('home.csv', mode='w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(home)

    blue.set_joint_positions(home)

    while True:
        which = np.random.randint(num_points)
        start_pos = recorded_positions[which]

        for i in range(resolution + 1):
            step = home + (start_pos - home) * cheb_points(resolution, i)
            blue.set_joint_positions(step)
            time.sleep(duration * 1.0 / resolution)

        time.sleep( end_pause )

        for i in range(resolution + 1):
            step = start_pos + (home - start_pos) * cheb_points(resolution, i)
            blue.set_joint_positions(step)
            time.sleep(duration * 1.0 / resolution)

        blue.set_joint_positions(home)
        time.sleep( end_pause )

blue.cleanup()
