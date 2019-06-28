# blue_interface
blue_interface is a high-level Python API that allows users to control a Blue robotic arm without directly interfacing with ROS. It uses [rosbridge](https://github.com/RobotWebTools/rosbridge_suite) to communicate with Blue's ROS-based control system over a network connection.

### Why use blue_interface?
- No dependency on ROS
- Easy to connect to multiple robots
- Works with both Python 2 and 3
- Works with Mac, Windows, and Linux
- Works in Jupyter Notebooks

### Installing with pip
```
git clone https://github.com/berkeleyopenarms/blue_interface.git
cd blue_interface
pip install -e .
```

### Examples (`blue_interface/examples`)
  - `gripper_controller.py` - An example of opening and closing Blue's gripper.
  - `inverse_kinematics.py` - An example of sending Blue an end effector pose command.
  - `print_status.py` - An example of reading state and printing values from Blue.
  - `zero_position.py` - An example of sending Blue a command in joint space.

### API Documentation
https://berkeleyopenarms.github.io/blue_interface/

