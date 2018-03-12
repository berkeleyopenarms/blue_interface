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
        """IConstructer for KokoInterface.

        Args:
            ip (str): The Koko IP address. Defaults to 9090.
            port (int, optional): The Websocket port number for rosbridge.
        """
        self._RBC = ROSBridgeClient(ip, port)

        # ROS Topic Names
        _ROS_JOINT_POSITIONS_TOPIC = "/koko_controllers/joint_positions_controller/command"
        _ROS_JOINT_STATE_TOPIC = "/joint_states"
        _ROS_CARTESIAN_POSE_TOPIC = "/koko_controllers/cartesian_pose_controller/command"
        _ROS_TF_TOPIC = "/tf"

        # Frame names
        self._WORLD_FRAME = "base_link"
        self._END_EFFECTOR_FRAME = "forearm_link"

        self.joint_positions = None
        self.cartesian_pose = None
        self.joint_torques = None
        self.joint_velocities = None
        self.control_mode = KokoControlMode.JOINT_POSITIONS # controller started in launch file
        self._joint_names = ["base_roll_joint", "shoulder_lift_joint", "shoulder_roll_joint", "elbow_lift_joint", "elbow_roll_joint", "wrist_lift_joint", "wrist_roll_joint"]
        self._controller_lookup = {KokoControlMode.CONTROL_OFF: [],
                                KokoControlMode.JOINT_POSITIONS: ["/koko_controllers/joint_positions_controller"],
                                KokoControlMode.CARTESIAN_POSE: ["/koko_controllers/cartesian_pose_controller"],
                                KokoControlMode.TORQUE: ["/koko_controllers/torque_controller"],
                                KokoControlMode.VELOCITY: ["koko_controllers/velocity_controller"]}

        # Create Subscribers, Publishers, and Service Clients
        self._joint_state_subscriber = self._RBC.subscriber(_ROS_JOINT_STATE_TOPIC, "sensor_msgs/JointState", self._joint_state_callback)
        self._joint_positions_publisher = self._RBC.publisher(_ROS_JOINT_POSITIONS_TOPIC, "std_msgs/Float64MultiArray")
        self._tf_service_client = self._RBC.service("/republish_tfs", "tf2_web_republisher/RepublishTFs")
        self._cartesian_pose_publisher = self._RBC.publisher(_ROS_CARTESIAN_POSE_TOPIC, "geometry_msgs/PoseStamped")
        self._switch_controller_service_client = self._RBC.service("controller_manager/switch_controller", "controller_manager_msgs/SwitchController")

        self._call_tf_service()

        while self.cartesian_pose == None or self.joint_positions == None or self.joint_torques == None or self.joint_velocities == None:
            time.sleep(0.1)

    def set_joint_positions(self, joint_positions):
        """Move arm to specified position in joint space.

        Args:
            joint_positions: A numpy array of 7 joint angles, in radians, ordered from proximal to distal.
        """
        if self.control_mode == KokoControlMode.JOINT_POSITIONS:
            joint_positions_msg = {
                "layout" : {},
                "data": joint_positions
            }

            self._joint_positions_publisher.publish(joint_positions_msg)
        else:
            warnings.warn("KokoControlMode is not JOINT_POSITIONS.")

    def set_cartesian_pose(self, target_pose):
        """Move end effector to specified pose in Cartesian space.

        Args:
            target_pose: Pose in the form {"position": numpy.array([x,y,z]), "orientation": numpy.array([x,y,z,w]} defined with respect to the world frame.
        """
        if self.control_mode == KokoControlMode.CARTESIAN_POSE:
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
        else:
            warnings.warn("KokoControlMode is not CARTESIAN_POSE.")

    def set_control_mode(self, mode):
        """Switch between available control modes.

        Args:
            mode: A KokoControlMode member indicating the desired control mode.

        Returns:
            bool: True if successful in setting the control mode. False otherwise.
        """
        if mode == self.control_mode:
            return True
        request_msg = {
            "start_controllers": self._controller_lookup[mode],
            "stop_controllers": self._controller_lookup[self.control_mode],
            "strictness": 2 #strict
        }

        s = threading.Semaphore(0)

        def switch_controller_callback(success, values):
            if success:
                self.control_mode = mode
            s.release()

        self._switch_controller_service_client.request(request_msg, switch_controller_callback)
        s.acquire()

        return mode == self.control_mode

    def get_joint_positions(self):
        """Get the current joint positions.

        Returns:
            A list of 7 angles, in radians, ordered from proximal to distal.
        """
        return np.array(self.joint_positions)

    def get_cartesian_pose(self):
        """Get the current cartesian pose of the end effector with respect to the world frame.

        Returns:
             Pose in the form {"position": numpy.array([x,y,z]), "orientation": numpy.array([x,y,z,w]} defined with repect to the world frame.
        """
        return self.cartesian_pose

    def get_joint_torques(self):
        """Get the current joint torques.

        Returns:
            A numpy array of 7 joint torques, in Nm, ordered from proximal to distal.
        """
        return np.array(self.joint_torques)

    def get_joint_velocities(self):
        """Get the current joint velocities.

        Returns:
            A numpy array of 7 joint velocities, in m/s, ordered from proximal to distal.
        """
        return np.array(self.joint_velocities)

    def get_control_mode(self):
        """Get the current control mode of the arm.

        Returns:
            A KokoControlMode object.
        """
        return self.control_mode

    def _joint_state_callback(self, message):
        self._joint_positions_callback(self, message)
        self._joint_torques_callback(self, message)
        self._joint_velocities_callback(self, message)

    def _joint_positions_callback(self, message):
        joint_positions_temp = []
        for name in self._joint_names:
            if name not in message.keys():
                break
            self.index = message["name"].index(name)
            joint_positions_temp.append(message["position"][self.index])
        self.joint_positions = joint_positions_temp

    def _joint_torques_callback(self, message):
        joint_torques_temp = []
        for name in self._joint_names:
            if name not in message.keys():
                break
            self.index = message["name"].index(name)
            joint_torques_temp.append(message["effort"][self.index])
        self.joint_torques = joint_torques_temp

    def _joint_velocities_callback(self, message):
        joint_velocities_temp = []
        for name in self._joint_names:
            if name not in message.keys():
                break
            self.index = message["name"].index(name)
            joint_velocities_temp.append(message["velocity"][self.index])
        self.joint_velocities = joint_velocities_temp

    def _process_tfs(self, message):
        pose = message["transforms"][0]["transform"]
        trans = pose["translation"]
        rot = pose["rotation"]
        cartesian_pose_temp = {}
        cartesian_pose_temp["position"] = np.array([trans["x"], trans["y"], trans["z"]])
        cartesian_pose_temp["orientation"] = np.array([rot["x"], rot["y"], rot["z"], rot["w"]])
        self.cartesian_pose = cartesian_pose_temp

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

class KokoControlMode(Enum):
    # TODO add torque control mode
    """An Enum class for constants that specify control mode.

    Attributes:
        CONTROL_OFF: Koko is in gravity componesation mode and can be manually manipulated.
        JOINT_POSITIONS: Koko can be controlled by sending joint position targets.
        CARTESIAN_POSE: Koko can be controlled by sending cartesian pose targets. 
    """
    CONTROL_OFF = 0
    JOINT_POSITIONS = 1
    CARTESIAN_POSE = 2
    TORQUE = 3
    VELOCITY = 4
