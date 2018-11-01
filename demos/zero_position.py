#!/usr/bin/env python3

# A basic example of using BlueInterface for joint positions control.
# It allows a user to record four sets of joint positions by manually moving the arm to each
# position and pressing enter. It then plays back a trajectory comprised of the four sets of
# joint positions in an infinite loop.

import sys
sys.path.append('../')
from blue_interface import BlueInterface
import numpy as np
import time

if __name__ == '__main__':
    arm = "right"
    address = "127.0.0.1"

    blue = BlueInterface(arm, address)
    blue.set_joint_positions(np.zeros(7))

    while True:
        pass
    # blue.shutdown()
