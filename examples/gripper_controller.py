#!/usr/bin/env python3

# A basic example of using BlueInterface for gripper control.
# It allows a user to open and close the gripper.

import numpy as np

from blue_interface import BlueInterface

side = "right"
ip = "127.0.0.1"
blue = BlueInterface(side, ip)

# After calibration, the gripper will be closed
blue.calibrate_gripper()

opened = False
while True:
    input("Press enter to open/close the gripper. To exit, press <ctrl+c>.")

    if opened:
        print("Closing...")
        blue.command_gripper(-1.5, 20.0, wait=True)
    else:
        print("Opening...")
        blue.command_gripper(0.0, 10.0, wait=True)

    opened = not opened
