# blue_interface
blue_interface is a Python API that allows users to control a Blue robotic arm without directly interfacing with ROS. It uses rosbridge to communicate with the Blue arm's onboard robot computer.

### Installing with pip
```
git clone https://github.com/berkeleyopenarms/blue_interface.git
cd blue_interface
pip install -e .
```

### Examples (`blue_interface/examples`)
  - `gripper_controller.py` - An example of opening and closing Blue's gripper.
  - `print_status.py` - An example of reading state and printing values from Blue.
  - `zero_position.py` - An example of sending Blue a joint position command.

### API Documentation
https://berkeleyopenarms.github.io/blue_interface/

