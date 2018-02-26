#!/usr/bin/env python3
from rosbridge_client import ROSBridgeClient
import time
import warnings
from enum import Enum

class KokoInterface:

    def __init__(self, ip, port=9090):
        self._RBC = ROSBridgeClient(ip, port)

        # ROS Topic Names
        _ROS_SET_JOINT_POSITIONS_TOPIC = "/koko_controllers/joint_positions_controller/command"
        _ROS_JOINT_STATE_TOPIC = "/joint_states"
        _ROS_SET_CARTESIAN_POSE_TOPIC = "/koko_controllers/cartesian_pose_controller/command"
        _ROS_SET_P_TERMS_TOPIC = "/p_terms" # temporary
        _ROS_SET_D_TERMS_TOPIC = "/d_terms" # temporary

        self.joint_positions = None
        self.cartesian_pose = None
        self.control_mode = KokoControlMode.JOINT_POSITIONS # controller started in launch file
        self._joint_names = ["base_roll_joint", "shoulder_lift_joint", "shoulder_roll_joint", "elbow_lift_joint", "elbow_roll_joint", "wrist_lift_joint", "wrist_roll_joint"]

        # Create Subscribers, Publishers, and Service Clients
        self._joint_state_subscriber = self._RBC.subscriber(_ROS_JOINT_STATE_TOPIC, "sensor_msgs/JointState", self._joint_positions_callback)
        self._joint_positions_publisher = self._RBC.publisher(_ROS_SET_JOINT_POSITIONS_TOPIC, "std_msgs/Float64MultiArray")
        self._cartesian_pose_publisher = self._RBC.publisher(_ROS_SET_CARTESIAN_POSE_TOPIC, "geometry_msgs/PoseStamped")
        self._p_terms_publisher = self._RBC.publisher(_ROS_SET_P_TERMS_TOPIC, "std_msgs/Float64MultiArray")
        self._d_terms_publisher = self._RBC.publisher(_ROS_SET_D_TERMS_TOPIC, "std_msgs/Float64MultiArray")
        self._switch_controller_service_client = self._RBC.service("controller_manager/switch_controller", "controller_manager_msgs/SwitchController")

        while self.joint_positions == None:
            time.sleep(0.1)

    def set_joint_positions(self, joint_positions):
        """
        Moves arm to specified positions in joint space.

        @param joint_positions: a list of 7 joint angles, in radians, ordered from proximal to distal
        """
        if self.control_mode == KokoControlMode.JOINT_POSITIONS:
            joint_positions_msg = {
                "layout" : {},
                "data": joint_positions
            }

            self._joint_positions_publisher.publish(joint_positions_msg)
        else:
            warnings.warn("KokoControlMode is not JOINT_POSITIONS.")

    def set_cartesian_pose(self, position, orientation):
        """
        Moves end effector to specified pose in Cartesian space.

        @param position: a list containing Cartesian coordinates in the base_link frame
        @param orientation: a quaternion defined in the base_link frame
        """
        if self.control_mode == KokoControlMode.CARTESIAN_POSE:
            position_msg = {
                "x": position[0],
                "y": position[1],
                "z": position[2]
            }

            orientation_msg = {
                "x": orientation[0],
                "y": orientation[1],
                "z": orientation[2],
                "w": orientation[3]
            }

            pose_msg = {
                "position": position_msg,
                "orientation": orientation_msg
            }

            cartesian_pose_msg = {
                "header": {},
                "pose": pose_msg
            }

            self.set_cartesian_pose_publisher.publish(cartesian_pose_msg)
        else:
            warnings.warn("KokoControlMode is not CARTESIAN_POSE.")

    def get_joint_positions(self):
        """
        Returns the current position of the arm in joint space.

        @return: a list of 7 angles, in radians, ordered from proximal to distal
        """
        return self.joint_positions

    def set_control_mode(self, mode):
        # TODO add torque control mode
        """
        Allows user to switch between available control modes.

        @param mode: a KokoControlMode member -- CONTROL_OFF, JOINT_POSITIONS, or CARTESIAN_POSE
        @return: a boolean that indicates success in setting the control mode
        """
        if mode == self.control_mode:
            return

        if self.control_mode == Koko_ControlMode.CONTROL_OFF:
            if mode == KokoControlMode.JOINT_POSITIONS:
                request_msg = {
                    "start_controllers": ["koko_controllers/joint_position_controller"],
                    "stop_controllers": [],
                    "strictness": 2 # Strict
                }

            elif mode == KokoControlMode.CARTESIAN_POSE:
                request_msg = {
                    "start_controllers": ["koko_controllers/cartesian_pose_controller"],
                    "stop_controllers": [],
                    "strictness": 2 # Strict
                }

        elif self.control_mode == KokoControlMode.JOINT_POSITIONS:
            if mode == KokoControlMode.CONTROL_OFF:
                request_msg = {
                    "start_controllers": [],
                    "stop_controllers": ["koko_controllers/joint_position_controller"],
                    "strictness": 2 # Strict
                }

            elif mode == KokoControlMode.CARTESIAN_POSE:
                request_msg = {
                    "start_controllers": ["koko_controllers/cartesian_pose_controller"],
                    "stop_controllers": ["koko_controllers/joint_position_controller"],
                    "strictness": 2 # Strict
                }

        elif self.control_mode == KokoControlMode.CARTESIAN_POSE:
            if mode == KokoControlMode.CONTROL_OFF:
                request_msg = {
                    "start_controllers": [],
                    "stop_controllers": ["koko_controllers/cartesian_pose_controller"],
                    "strictness": 2 # Strict
                }

            if mode == KokoControlMode.JOINT_POSITIONS:
                request_msg = {
                    "start_controllers": ["koko_controllers/joint_position_controller"],
                    "stop_controllers": ["koko_controllers/cartesian_pose_controller"],
                    "strictness": 2 # Strict
                }

        def switch_controller_callback(message):
            if message == 1:
                self.control_mode = mode

        self._switch_controller_service_client.request(request_msg, switch_controller_callback)

        return mode == self.control_mode

    def disable_control(self):
        # TODO temporary, will be replaced with set_control_mode functionality
        p_terms_msg = {
            "layout" : {},
            "data": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        }

        d_terms_msg = {
            "layout" : {},
            "data": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        }

        self._p_terms_publisher.publish(p_terms_msg)
        self._d_terms_publisher.publish(d_terms_msg)

    def enable_control(self):
        # TODO temporary, will be replaced with set_control_mode functionality
        p_terms_msg = {
            "layout" : {},
            "data": [25.0, 25.0, 15.0, 15.0, 10.0, 5.0, 5.0]
        }

        d_terms_msg = {
            "layout" : {},
            "data": [3.0, 4.0, 3.0, 2.0, 2.0, 1.0, 1.0]
        }

        self._p_terms_publisher.publish(p_terms_msg)
        self._d_terms_publisher.publish(d_terms_msg)

    def _joint_positions_callback(self, message):
        joint_positions_temp = []
        for name in self._joint_names:
            self.index = message["name"].index(name)
            joint_positions_temp.append(message["position"][self.index])
        self.joint_positions = joint_positions_temp


class KokoControlMode(Enum):
    # TODO add torque control mode
    CONTROL_OFF = 0
    JOINT_POSITIONS = 1
    CARTESIAN_POSE = 2
