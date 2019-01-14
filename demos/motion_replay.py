#!/usr/bin/python3

import pickle  # will use to save data between program launches
import sys
import numpy as np
import time
import argparse
from blue_interface import BlueInterface  # this is the API for the robot

import consts

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Replay motion on a blue arm.')
    parser.add_argument('record_file', type=str, help='Loads a recorded motion from this file')
    parser.add_argument('--address', default=consts.default_address, type=str, help='Address of the host computer')
    parser.add_argument('--port', default=consts.default_port, type=int, help='Port that the ros web host was started on')
    parser.add_argument('--frequency', default=0, type=int, help='Replay the recording at a custom frequency (Hz)')
    args = parser.parse_args()

    filename = args.record_file

    arm = consts.default_arm
    address = args.address
    port = args.port

    #blue = BlueInterface("left","10.42.0.1")  # creates object of class KokoInterface at the IP in quotes with the name 'blue'
    blue = BlueInterface(arm, address, port) #creates object of class KokoInterface at the IP in quotes with the name 'blue'

    # This turns off any other control currently on the robot (leaves it in gravtiy comp mode)
    blue.disable_control()

    data = pickle.load( open(filename, "rb")) #uses the pickle function to read the binary file created in record_poses.py
    joint_angle_list, _, gripper_list, record_frequency = data

    # If no argument is passed for replay frequency, play the recording at the rate it was recorded.
    if args.frequency == 0:
        frequency = record_frequency # In Hertz

    input("Press enter to start replay. To exit, press <ctrl+c>.")

    try:
        last_time = 0.0
        for i in range (len(joint_angle_list)):
            #if len(joint_angle_list[i]) == 7:
            blue.set_joint_positions(np.array(joint_angle_list[i])) # tell the robot to go to a set of joint angles
            #blue.command_gripper(gripper_list[i], 30.0)
            if gripper_list[i] < -0.2:
                blue.command_gripper(-1.3, 15.0)
            else:
                blue.command_gripper(0, 2.0)
            sleep_time = 1.0/frequency - (time.time() - last_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
            last_time = time.time()

    except:
        print (sys.exc_info()[0])
        print ("Something went wrong... exiting")
        pass

    time.sleep(2)
    blue.shutdown()
