#!/usr/bin/env python3

# A basic example of using BlueInterface for joint positions control.
# It allows a user to record four sets of joint positions by manually moving the arm to each
# position and pressing enter. It then plays back a trajectory comprised of the four sets of
# joint positions in an infinite loop.

import sys
from blue_interface import BlueInterface
import numpy as np
import time

side = "right"
ip = "127.0.0.1"
blue = BlueInterface(side, ip)

blue.set_joint_positions(np.zeros(7), duration=3.0)

while True:
    pass

# When this script terminates (eg via Ctrl+C), the robot will automatically
# stop all controllers and go back to gravity compensation mode

