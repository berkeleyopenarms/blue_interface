# blue_interface
blue_interface is a Python API that allows users to control a Blue robotic arm without directly interfacing with ROS. It uses rosbridge to communicate with the Blue arm's onboard computer. The following files are included in this repository:
  - blue_interface.py: A file containing methods for controlling a Blue arm in joint position, joint torque, and cartesian pose control modes
  - Demos
    - rosbridge_client.py: A client that provides basic ROS functionality using rosbridge
    - record_positions_example.py: A Hello World for controlling a Blue arm with joint position control
    - record_pose_example.py: A Hello World for controlling a Blue arm with carteisian pose control
    - gripper_example.py: A Hello World for commanding a Blue arm's gripper
    - motion_record.py and motion_replay.py: A pair of scripts that record the state of the arm and then replay that motion.
    - consts.py: These values set up default arguments when running demo scripts. Adjust as needed!
    
# Use of Recording
To record a motion, execute `python3 motion_record.py <file_name.pickle>`. To replay a motion, execute `python3 motion_replay.py <file_name.pickle>`. These can be executed from any computer with access to the control computer via an internet connection (i.e. LAN).

# Documentation
https://berkeley-open-robotics.github.io/blue_interface/

# Required Python Packages
  - ws4py (`pip install ws4py`)
  - PyDispatcher (`pip install PyDispatcher`)
  
