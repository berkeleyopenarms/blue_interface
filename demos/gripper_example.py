#!/usr/bin/env python3

# A basic example of using BlueInterface for gripper control.
# It allows a user to open and close the gripper.

from blue_interface import BlueInterface
import numpy as np

blue = BlueInterface("right", "hekate.cs.berkeley.edu")
while True:
    blue.command_gripper(0.0,2.0,True)
    blue.command_gripper(-1.3,2.0,True)

