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
        _ROS_POSITION_TOPIC = "/koko_controllers/position_controller/command"
        _ROS_TORQUE_TOPIC = "/koko_controllers/torque_controller/command"
        _ROS_VELOCITY_TOPIC = "/koko_controllers/velocity_controller/command"
        _ROS_JOINT_STATE_TOPIC = "/joint_states"
        _ROS_POSE_TOPIC = "/koko_controllers/cartesian_pose_controller/command"
        _ROS_TF_TOPIC = "/tf"

        # Frame names
        self._WORLD_FRAME = "base_link"
        self._END_EFFECTOR_FRAME = "forearm_link"

        # TODO: since we have getters for many of these variables,
        #       we can probably make them private
        self.joint_positions = None
        self.cartesian_pose = None
        self.joint_torques = None
        self.joint_velocities = None

        # TODO: does the user need to access the control mode? this can probably be private
        self.control_mode = KokoControlMode.OFF

        self._joint_names = ["base_roll_joint", "shoulder_lift_joint", "shoulder_roll_joint", "elbow_lift_joint", "elbow_roll_joint", "wrist_lift_joint", "wrist_roll_joint"]
        self._controller_lookup = { KokoControlMode.OFF: [],
                                    KokoControlMode.POSITION: ["/koko_controllers/position_controller"],
                                    KokoControlMode.POSE: ["/koko_controllers/cartesian_pose_controller"],
                                    KokoControlMode.TORQUE: ["/koko_controllers/torque_controller"],
                                    KokoControlMode.VELOCITY: ["koko_controllers/velocity_controller"] }

        # Create Subscribers, Publishers, and Service Clients
        self._joint_state_subscriber = self._RBC.subscriber(_ROS_JOINT_STATE_TOPIC, "sensor_msgs/JointState", self._joint_state_callback)
        self._joint_position_publisher = self._RBC.publisher(_ROS_POSITION_TOPIC, "std_msgs/Float64MultiArray")
        self._joint_torque_publisher = self._RBC.publisher(_ROS_TORQUE_TOPIC, "std_msgs/Float64MultiArray")
        self._joint_velocity_publisher = self._RBC.publisher(_ROS_VELOCITY_TOPIC, "std_msgs/Float64MultiArray")
        self._tf_service_client = self._RBC.service("/republish_tfs", "tf2_web_republisher/RepublishTFs")
        self._cartesian_pose_publisher = self._RBC.publisher(_ROS_POSE_TOPIC, "geometry_msgs/PoseStamped")
        self._switch_controller_service_client = self._RBC.service("controller_manager/switch_controller", "controller_manager_msgs/SwitchController")

        self._call_tf_service()

        # TODO: consider using condition variable instead of busy-waiting
        while self.cartesian_pose == None or self.joint_positions == None or self.joint_torques == None or self.joint_velocities == None:
            time.sleep(0.1)

    def set_joint_positions(self, joint_positions):
        """Move arm to specified position in joint space.

        Args:
            joint_positions: A numpy array of 7 joint angles, in radians, ordered from proximal to distal.
        """

        # TODO: maybe move this if statement into _set_control_mode
        if self.control_mode != KokoControlMode.POSITION:
            self._set_control_mode(KokoControlMode.POSITION)

        # TODO: check validity of commands
        # assert type(joint_positions) == np.ndarray
        # assert joint_positions.shape == (self.joint_positions,)
        # etc
        # same for other commands

        joint_positions_msg = {
            "layout" : {},
            "data": list(joint_positions)
        }

        self._joint_position_publisher.publish(joint_positions_msg)

    def set_joint_torques(self, joint_torques):
        """Set torques applied at joints.

        Args:
            joint_torques: A numpy array of 7 joint torques, in Nm, ordered from proximal to distal.
        """
        if self.control_mode != KokoControlMode.TORQUE:
            self._set_control_mode(KokoControlMode.TORQUE)

        joint_torques_msg = {
            "layout" : {},
            "data": joint_torques
        }

        self._joint_torque_publisher.publish(joint_torques_msg)

    def set_joint_velocities(self, joint_velocities):
        """Set velocities of joints.

        Args:
            joint_velocities: A numpy array of 7 joint velocities, in m/s, ordered from proximal to distal.
        """
        if self.control_mode != KokoControlMode.VELOCITY:
            self._set_control_mode(KokoControlMode.VELOCITY)

        joint_velocities_msg = {
            "layout" : {},
            "data": joint_velocities
        }

        self._joint_velocity_publisher.publish(joint_velocities_msg)

    def set_cartesian_pose(self, target_pose):
        """Move end effector to specified pose in Cartesian space.

        Args:
            target_pose: Pose in the form {"position": numpy.array([x,y,z]), "orientation": numpy.array([x,y,z,w]} defined with respect to the world frame.
        """
        if self.control_mode == KokoControlMode.POSE:
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
            warnings.warn("KokoControlMode is not POSE.")

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

    def disable_control(self):
        """Set control mode to gravity compensation only."""
        self._set_control_mode(KokoControlMode.OFF)

    def _joint_state_callback(self, message):
        joint_positions_temp = []
        joint_torques_temp = []
        joint_velocities_temp = []
        for name in self._joint_names:
            if name not in message.keys():
                break
            self.index = message["name"].index(name)
            joint_positions_temp.append(message["position"][self.index])
            joint_torques_temp.append(message["effort"][self.index])
            joint_velocities_temp.append(message["velocity"][self.index])
        self.joint_positions = joint_positions_temp
        self.joint_torques = joint_torques_temp
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

    def _set_control_mode(self, mode):
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


# TODO: this can be abstracted away from the user; make it private
class KokoControlMode(Enum):
    """An Enum class for constants that specify control mode.

    Attributes:
        OFF: Koko is in gravity componesation mode and can be manually manipulated.
        POSITION: Koko can be controlled by sending joint position targets.
        POSE: Koko can be controlled by sending cartesian pose targets.
        TORQUE: Koko can be controlled by setting joint torque targets.
        VELOCITY: Koko can be controlled by setting joint velocity targets.
    """
    OFF = 0
    POSITION = 1
    POSE = 2
    TORQUE = 3
    VELOCITY = 4
