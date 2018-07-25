# blue_interface
blue_interface is a Python API that allows users to control a Blue robotic arm without directly interfacing with ROS. It uses rosbridge to communicate with the Blue arm's onboard robot computer. The entire Python API is contained in `blue_interface.py`, and includes methods for controlling a Blue arm in joint position, joint torque, and Cartesian pose control modes.

# Required Python 3 Packages
  - ws4py (`pip install ws4py`)
  - PyDispatcher (`pip install PyDispatcher`)
  - numpy (`pip install numpy`)

# Demos (`blue_interface/demos`)
  - motion_record.py and motion_replay.py - A pair of scripts that record the state of the arm and then replay that motion.
    - To record a motion, execute `python3 motion_record.py <file_name.pickle>`.
    - To replay a motion, execute `python3 motion_replay.py <file_name.pickle>`.
    - These can be executed from any computer with access to the control computer via an internet connection (i.e. LAN).
  - rosbridge_client.py - A client that provides basic ROS functionality using rosbridge
  - record_positions_example.py - A Hello World for controlling a Blue arm with joint position control
  - record_pose_example.py - A Hello World for controlling a Blue arm with Cartesian pose control
  - gripper_example.py - A Hello World for commanding a Blue arm's gripper
  - consts.py - These values set up default arguments when running demo scripts. Adjust as needed!

# API Documentation
https://berkeley-open-robotics.github.io/blue_interface/
  
