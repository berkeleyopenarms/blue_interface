#!/usr/bin/env python3

# A basic example of using BlueInterface for joint positions control.
# It allows a user to record four sets of joint positions by manually moving the arm to each
# position and pressing enter. It then plays back a trajectory comprised of the four sets of
# joint positions in an infinite loop.

import sys
from blue_interface import BlueInterface
import numpy as np
import time
import pickle
import argparse
import consts

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replay a blue arm through a recorded set of positions.')
    parser.add_argument('--tape_file', default = 'tape_trajectory.pickle', type=str, help='Saves a set of positions to this file')
    parser.add_argument('--address', default=consts.default_address, type=str, help='Address of the host computer')
    parser.add_argument('--port', default=consts.default_port, type=int, help='Port that the ros web host was started on')
    args = parser.parse_args()

    arm = consts.default_arm
    address = args.address
    port = args.port
    filename = args.tape_file

    blue = BlueInterface(arm, address, port) #creates object of class KokoInterface at the IP in quotes with the name 'blue'

    print("..")
    recorded_positions = []
    error = 0.5

    blue.disable_control()
    blue.disable_gripper()

    #TODO: make number of positions a command line arg
    with open(filename, 'rb') as handle:
        recorded_positions = pickle.load(handle)

    input("Press enter to start trajectory.")

    while True:
        for desired_position in recorded_positions:
            current_position = (blue.get_gripper_position(), blue.get_joint_positions())
            blue.set_joint_positions(np.array(desired_position[1]))
            blue.command_gripper(desired_position[0], 2.0, True)
            while np.linalg.norm(desired_position[1] - current_position[1]) > error:
                current_position = (blue.get_gripper_position(), blue.get_joint_positions())
                time.sleep(0.1)
