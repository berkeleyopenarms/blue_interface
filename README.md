# blue_interface

[
**[API Reference](https://blue-interface.readthedocs.io)**
] [
**[Examples](https://github.com/berkeleyopenarms/blue_interface/tree/master/examples)**
]


![robot arm splash](https://brentyi.github.io/filestore/blue_single_arm_resized.png)

![build](https://github.com/berkeleyopenarms/blue_interface/workflows/build/badge.svg)
![mypy](https://github.com/berkeleyopenarms/blue_interface/workflows/mypy/badge.svg?branch=master)
![lint](https://github.com/berkeleyopenarms/blue_interface/workflows/lint/badge.svg)

Blue Interface is a platform-agnostic Python API for controlling Blue robotic
arms. It uses [rosbridge](https://github.com/RobotWebTools/rosbridge_suite) to
communicate with Blue's ROS-based control system over a network connection.

**Features:**

- No dependency on ROS (or any particular version of Ubuntu)
- Easy connection to multiple robots
- Support for both Python 2 and 3
- Support for Mac, Windows, and Linux
- Support for Jupyter Notebooks

It's designed to be lightweight and easy-to-use! Sending a Blue "right" arm to
its zero position, for example, is as simple as:

```python
from blue_interface import BlueInterface

blue = BlueInterface(side="right", ip="127.0.0.1")
blue.set_joint_positions([0] * 7)
```

### Installation

From PyPi:

```sh
pip install blue_interface
```

From source:

```sh
git clone https://github.com/berkeleyopenarms/blue_interface.git
cd blue_interface
pip install -e .
```

### Examples

- `gripper_controller.py` - An example of opening and closing Blue's gripper.
- `inverse_kinematics.py` - An example of sending Blue an end effector pose
  command.
- `print_status.py` - An example of reading state and printing values from Blue.
- `zero_position.py` - An example of sending Blue a command in joint space.
