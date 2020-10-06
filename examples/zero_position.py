#!/usr/bin/env python3

# A basic example of using BlueInterface for joint positions control.

import numpy as np

from blue_interface import BlueInterface

side = "right"
ip = "127.0.0.1"
blue = BlueInterface(side, ip)

blue.set_joint_positions(np.zeros(7), duration=3.0)

while True:
    pass

# When this script terminates (eg via Ctrl+C), the robot will automatically
# stop all controllers and go back to gravity compensation mode
