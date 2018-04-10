#!/usr/bin/env python3
from rosbridge_client import ROSBridgeClient
import time
import warnings
import threading
from enum import Enum
import numpy as np

class KokoInterface:
    """An Python interface for controling a Koko robot through ROSBridge."""

    def __init__(self, ip, port=9090):
        """Constructer for KokoInterface.

        Args:
            ip (str): The Koko IP address. Defaults to 9090.
            port (int, optional): The Websocket port number for rosbridge.
        """
        self._RBC = ROSBridgeClient(ip, port)
        # ROS Topic Names
        _ROS_POSITION_TOPIC = "/koko_controllers/joint_position_controller/command"
        _ROS_TORQUE_TOPIC = "/koko_controllers/torque_controller/command"
        _ROS_JOINT_STATE_TOPIC = "/joint_states"
        _ROS_POSE_TOPIC = "/koko_controllers/cartesian_pose_controller/command"
        _ROS_GRIPPER_TOPIC = "/koko_controllers/gripper_controller/gripper_cmd"
        _ROS_TF_TOPIC = "/tf"

        # Frame names
        self._WORLD_FRAME = "base_link"
        self._END_EFFECTOR_FRAME = "forearm_link"

        self._joint_positions = None
        self._cartesian_pose = None
        self._joint_torques = None
        self._gripper_goal_id = None
        self._gripper_position = None
        self._gripper_effort = None

        sell._control_mode = _KokoControlMode.OFF

        self._joint_names = ["base_roll_joint", "shoulder_lift_joint", "shoulder_roll_joint", "elbow_lift_joint", "elbow_roll_joint", "wrist_lift_joint", "wrist_roll_joint"]
        self._controller_lookup = { _KokoControlMode.OFF: [],
                                    _KokoControlMode.POSITION: ["koko_controllers/joint_position_controller"],
                                    _KokoControlMode.POSE: ["koko_controllers/cartesian_pose_controller"],
                                    _KokoControlMode.TORQUE: ["koko_controllers/torque_controller"]}

        # Create Subscribers, Publishers, and Service/Action Clients
        self._joint_state_subscriber = self._RBC.subscriber(_ROS_JOINT_STATE_TOPIC, "sensor_msgs/JointState", self._joint_state_callback)
        self._joint_position_publisher = self._RBC.publisher(_ROS_POSITION_TOPIC, "std_msgs/Float64MultiArray")
        self._joint_torque_publisher = self._RBC.publisher(_ROS_TORQUE_TOPIC, "std_msgs/Float64MultiArray")
        self._tf_service_client = self._RBC.service("/republish_tfs", "tf2_web_republisher/RepublishTFs")
        self._cartesian_pose_publisher = self._RBC.publisher(_ROS_POSE_TOPIC, "geometry_msgs/PoseStamped")
        self._switch_controller_service_client = self._RBC.service("controller_manager/switch_controller", "controller_manager_msgs/SwitchController")
        self._gripper_action_client = self._RBC.action_client(_ROS_GRIPPER_TOPIC, "control_msgs/GripperCommandAction")

        self._call_tf_service()

        while None in [self._cartesian_pose, self._joint_positions, self._joint_torques, self._gripper_position, self._gripper_effort]:
            time.sleep(.01)


    def command_gripper(self, position, effort):
        """Send a goal to gripper.

        Args:
            position (float64): gap size between gripper fingers in cm.
            effort (float64): maximum effort the gripper with exert before stalling in N.
        """

        goal_msg = {"command": {
            "position": position,
            "max_effort": effort
        }}

        self._gripper_goal_id = self._gripper_action_client.send_goal(goal_msg, None, None) #None should be fine let's see what's up

    def cancel_gripper_command(self):
        #TODO: test this!
        """Cancel current gripper command, halting gripper in current position."""

        self._gripper_action_client.cancel_goal(self._gripper_goal_id)

    def get_gripper_position(self):
        #TODO: test this
        """ Get the current gap between gripper fingers.

        Returns:
            float64: the gripper gap in cm.

        """
        return self._gripper_position

    def get_gripper_effort(self):
        #TODO: test this
        """Get the current effort exerted by the gripper.

        Returns:
            float64: the gripper effort in N
        """

        return self._gripper_effort

    def set_joint_positions(self, joint_positions):
        """Move arm to specified position in joint space.

        Args:
            joint_positions (numpy.ndarray): An array of 7 joint angles, in radians, ordered from proximal to distal.
        """

        self._set_control_mode(_KokoControlMode.POSITION)
        assert type(joint_positions) == np.ndarray, "joint_positions should be a numpy array"

        joint_positions_msg = {
            "layout" : {},
            "data": list(joint_positions)
        }
        self._joint_position_publisher.publish(joint_positions_msg)

    def set_joint_torques(self, joint_torques):
        """Set torques applied at joints.

        Args:
            joint_torques (numpy.ndarray): An array of 7 joint torques, in Nm, ordered from proximal to distal.
        """
        self._set_control_mode(_KokoControlMode.TORQUE)

        assert type(joint_torques) == np.ndarray, "joint_torques should be a numpy array"

        joint_torques_msg = {
            "layout" : {},
            "data": list(joint_torques)
        }

        self._joint_torque_publisher.publish(joint_torques_msg)

    def set_cartesian_pose(self, target_pose):
        """Move end effector to specified pose in Cartesian space.

        Args:
            target_pose (dict): Pose in the form {"position": numpy.array([x,y,z]), "orientation": numpy.array([x,y,z,w]} defined with respect to the world frame.
        """
        self._set_control_mode(_KokoControlMode.POSE)

        assert type(target_pose) == dict, "target_pose should be a python dictionary"
        assert type(target_pose["position"]) == np.ndarray, "position should be a numpy array"
        assert type(target_pose["orientation"]) == np.ndarray, "orientation should be a numpy array"

        position = target_pose["position"]
        orientation = target_pose["orientation"]
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

        self._cartesian_pose_publisher.publish(cartesian_pose_msg)

    def get_joint_positions(self):
        """Get the current joint positions.

        Returns:
            numpy.ndarray: An array of 7 angles, in radians, ordered from proximal to distal.
        """
        return self._joint_positions

    def get_cartesian_pose(self):
        """Get the current cartesian pose of the end effector with respect to the world frame.

        Returns:
            dict: Pose in the form {"position": numpy.array([x,y,z]), "orientation": numpy.array([x,y,z,w]} defined with repect to the world frame.
        """
        return self._cartesian_pose

    def get_joint_torques(self):
        """Get the current joint torques.

        Returns:
            numpy.ndarray: An array of 7 joint torques, in Nm, ordered from proximal to distal.
        """
        return self._joint_torques

    def disable_control(self):
        """Set control mode to gravity compensation only."""

        self._set_control_mode(_KokoControlMode.OFF)

    def _gripper_feedback_callback(self, message):
        #TODO: test this
        self._gripper_position = message["position"]
        self._gripper_effort = message["effort"]

    def _joint_state_callback(self, message):
        joint_positions_temp = []
        joint_torques_temp = []
        for name in self._joint_names:
            if name not in message["name"]:
                break
            self.index = message["name"].index(name)
            joint_positions_temp.append(message["position"][self.index])
            joint_torques_temp.append(message["effort"][self.index])
        self._joint_positions = np.array(joint_positions_temp)
        self._joint_torques = np.array(joint_torques_temp)

    def _process_tfs(self, message):
        pose = message["transforms"][0]["transform"]
        trans = pose["translation"]
        rot = pose["rotation"]
        cartesian_pose_temp = {}
        cartesian_pose_temp["position"] = np.array([trans["x"], trans["y"], trans["z"]])
        cartesian_pose_temp["orientation"] = np.array([rot["x"], rot["y"], rot["z"], rot["w"]])
        self._cartesian_pose = cartesian_pose_temp

    def _call_tf_service(self):
        goal_msg = {
            "source_frames": [self._END_EFFECTOR_FRAME],
            "target_frame": self._WORLD_FRAME,
            "angular_thres": 0,
            "trans_thres": 0,
            "rate": 2,
            "timeout": {"secs": 2.0, "nsecs": 0.0}
        }

        def _tf_service_callback(success, values):
            if success:
                self._tf_subscriber = self._RBC.subscriber(values["topic_name"], "tf2_web_republisher/TFArray", self._process_tfs)

        self._tf_service_client.request(goal_msg, _tf_service_callback)

    def _set_control_mode(self, mode):
        if mode == self._control_mode:
            return True
        request_msg = {
            "start_controllers": self._controller_lookup[mode],
            "stop_controllers": self._controller_lookup[self._control_mode],
            "strictness": 2 #strict
        }

        s = threading.Semaphore(0)

        def switch_controller_callback(success, values):
            if success:
                self._control_mode = mode
            s.release()

        self._switch_controller_service_client.request(request_msg, switch_controller_callback)
        s.acquire()

        return mode == self._control_mode


class _KokoControlMode(Enum):
    """An Enum class for constants that specify control mode.

    Attributes:
        OFF: Koko is in gravity componesation mode and can be manually manipulated.
        POSITION: Koko can be controlled by sending joint position targets.
        POSE: Koko can be controlled by sending cartesian pose targets.
        TORQUE: Koko can be controlled by setting joint torque targets.
    """
    OFF = 0
    POSITION = 1
    POSE = 2
    TORQUE = 3
