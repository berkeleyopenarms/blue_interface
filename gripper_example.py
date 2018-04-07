#!/usr/bin/env python3

# A basic example of using KokoInterface for joint positions control.
# It allows a user to record four sets of joint positions by manually moving the arm to each
# position and pressing enter. It then plays back a trajectory comprised of the four sets of
# joint positions in an infinite loop.

from koko_interface import KokoInterface
import numpy as np

koko = KokoInterface("hekate.cs.berkeley.edu")
print("made a Koko object")

koko.command_gripper(0.0,30.0)
koko.command_gripper(100.0,40.0)

