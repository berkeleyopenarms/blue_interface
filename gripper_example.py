#!/usr/bin/env python3

# A basic example of using KokoInterface for gripper control.
# It allows a user to open and close the gripper.

from koko_interface import KokoInterface
import numpy as np

#TODO: test it!
koko = KokoInterface("hekate.cs.berkeley.edu")
print("made a Koko object")

koko.command_gripper(0.0,2.0)
if koko.get_gripper_position() == 0.0:
    koko.command_gripper(-1.3,2.0)

