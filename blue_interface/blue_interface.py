from .rosbridge_client import ROSBridgeClient
import time
import warnings
import threading
from enum import Enum
import numpy as np
import atexit

class BlueInterface:
    """A Python interface for controlling the Blue robot through rosbridge."""

    def __init__(self, side, ip, port=9090):
        """Constructer for BlueInterface.

        Args:
            side (str): side of the arm "left"
            ip (str): The IP address of the robot, which by default should have a running rosbridge server.
            port (int, optional): The websocket port number for rosbridge. Defaults to 9090.
        """

        assert side == "left" or side == "right"

        self._RBC = ROSBridgeClient(ip, port)

        # ROS Topic Names
        topic_prefix = "/" + side + "_arm/"
        ROS_POSITION_TOPIC = topic_prefix + "blue_controllers/joint_position_controller/command"
        ROS_JOINT_STATE_TOPIC = "/joint_states"
        ROS_GRIPPER_TOPIC = topic_prefix + "blue_controllers/gripper_controller/gripper_cmd"
        ROS_TF_TOPIC = "/tf"

        # Frame names
        self._WORLD_FRAME = side + "_base_link"
        self._END_EFFECTOR_FRAME = side + "_end_roll_link"

        self._controller_lookup = { _BlueControlMode.OFF: "",
                                    _BlueControlMode.POSITION: "blue_controllers/joint_position_controller",
                                    _BlueControlMode.GRIPPER: "blue_controllers/gripper_controller"}

        self._joint_positions = None
        self._cartesian_pose = None
        self._joint_torques = None
        self._joint_velocities = None
        self._gripper_goal_id = None
        self._gripper_position = None
        self._gripper_effort = None

        self._joint_names = ["{}_{}".format(side, j) for j in [
            "base_roll_joint",
            "shoulder_lift_joint",
            "shoulder_roll_joint",
            "elbow_lift_joint",
            "elbow_roll_joint",
            "wrist_lift_joint",
            "wrist_roll_joint"
        ]]
        self._gripper_joint_name = side + "_gripper_joint"

        # Joint state pub/sub
        self._joint_state_subscriber = self._RBC.subscriber(ROS_JOINT_STATE_TOPIC, "sensor_msgs/JointState", self._joint_state_callback)
        self._joint_position_publisher = self._RBC.publisher(ROS_POSITION_TOPIC, "std_msgs/Float64MultiArray")

        # Controller manager services
        self._switch_controller_service_client = self._RBC.service(topic_prefix + "controller_manager/switch_controller", "controller_manager_msgs/SwitchController")
        self._load_controller_service_client = self._RBC.service(topic_prefix + "controller_manager/load_controller", "controller_manager_msgs/LoadController")
        self._unload_controller_service_client = self._RBC.service(topic_prefix + "controller_manager/unload_controller", "controller_manager_msgs/UnloadController")

        # TF repub service
        self._tf_service_client = self._RBC.service("/republish_tfs", "tf2_web_republisher/RepublishTFs")

        # Gripper action client
        self._gripper_action_client = self._RBC.action_client(ROS_GRIPPER_TOPIC, "control_msgs/GripperCommandAction")

        # Start listening to world->end effector transforms
        self._request_end_effector_tfs()

        # Load controllers
        self._load_controller(self._controller_lookup[_BlueControlMode.POSITION])
        self._load_controller(self._controller_lookup[_BlueControlMode.GRIPPER])

        # Cleaner exiting
        atexit.register(self.shutdown)

        # Make sure they're stopped
        self._switch_controller([], [self._controller_lookup[_BlueControlMode.POSITION], self._controller_lookup[_BlueControlMode.GRIPPER]])
        self._control_mode = _BlueControlMode.OFF
        self._gripper_enabled = False

        while self._cartesian_pose is None or self._joint_positions is None:
            time.sleep(.1)

    def shutdown(self, *unused):
        """Clean up and close connection to host computer."""
        print("shutdown")
        self._switch_controller([], [self._controller_lookup[_BlueControlMode.POSITION], self._controller_lookup[_BlueControlMode.GRIPPER]])
        self._unload_controller(self._controller_lookup[_BlueControlMode.POSITION])
        self._unload_controller(self._controller_lookup[_BlueControlMode.GRIPPER])
        self._RBC.close()

    def command_gripper(self, position, effort, wait=False):
        #TODO: change robot side so position and effort in correct units
        """Send a goal to gripper.

        Args:
            position (float64): gap size between gripper fingers in cm.
            effort (float64): maximum effort the gripper with exert before stalling in N.
        """

        if not self._gripper_enabled:
            self.enable_gripper()

        goal_msg = {"command": {
            "position": position,
            "max_effort": effort
        }}

        def on_result(result, status):
            if result["stalled"] or result["reached_goal"]:
                s.release()

        s = threading.Semaphore(0)
        self._gripper_goal_id = self._gripper_action_client.send_goal(goal_msg, on_result, on_result)
        if wait:
            s.acquire()

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
            joint_positions (iterable): An array of 7 joint angles, in radians, ordered from proximal to distal.
        """

        joint_positions = list(joint_positions)
        assert len(joint_positions) == 7

        self._set_control_mode(_BlueControlMode.POSITION)

        joint_positions_msg = {
            "layout" : {},
            "data": list(joint_positions)
        }
        self._joint_position_publisher.publish(joint_positions_msg)

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

    def get_joint_velocities(self):
        """Get the current joint velocities.

        Returns:
            numpy.ndarray: An array of 7 joint torques, in Nm, ordered from proximal to distal.
        """
        return self._joint_velocities

    def disable_control(self):
        """Set control mode to gravity compensation only."""

        self._set_control_mode(_BlueControlMode.OFF)

    def enable_gripper(self):
        """Enable gripper."""
        self._switch_controller([self._controller_lookup[_BlueControlMode.GRIPPER]], [])
        self._gripper_enabled = True

    def disable_gripper(self):
        """Make gripper compliant."""
        self._switch_controller([], [self._controller_lookup[_BlueControlMode.GRIPPER]])
        self._gripper_enabled = False

    def gripper_enabled(self):
        """Check if gripper is enabled to take commands.

        Returns:
            bool: True if enabled, False otherwise.
        """

        return self._gripper_enabled

    def _joint_state_callback(self, message):
        joint_positions_temp = []
        joint_torques_temp = []
        joint_velocities_temp = []

        for name in self._joint_names:
            if name not in message["name"]:
                continue
            else:
                self.index = message["name"].index(name)
                joint_positions_temp.append(message["position"][self.index])
                joint_torques_temp.append(message["effort"][self.index])
                joint_velocities_temp.append(message["velocity"][self.index])

        if self._gripper_joint_name in message["name"]:
            self._gripper_position = message["position"][message["name"].index(self._gripper_joint_name)]
            self._gripper_effort = message["effort"][message["name"].index(self._gripper_joint_name)]

        self._joint_positions = np.array(joint_positions_temp)
        self._joint_torques = np.array(joint_torques_temp)
        self._joint_velocities = np.array(joint_velocities_temp)

    def _process_tfs(self, message):
        pose = message["transforms"][0]["transform"]
        trans = pose["translation"]
        rot = pose["rotation"]
        cartesian_pose_temp = {}
        cartesian_pose_temp["position"] = np.array([trans["x"], trans["y"], trans["z"]])
        cartesian_pose_temp["orientation"] = np.array([rot["x"], rot["y"], rot["z"], rot["w"]])
        self._cartesian_pose = cartesian_pose_temp

    def _request_end_effector_tfs(self):
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
        self._switch_controller([self._controller_lookup[mode]], [self._controller_lookup[self._control_mode]], mode)
        return mode == self._control_mode

    def _switch_controller(self, start, stop, mode=None):
        request_msg = {
            "start_controllers": start,
            "stop_controllers": stop,
            "strictness": 1 # best effort
        }

        s = threading.Semaphore(0)

        def callback(success, values):
            if success and mode is not None:
                self._control_mode = mode
            s.release()

        self._switch_controller_service_client.request(request_msg, callback)
        s.acquire()

    def _load_controller(self, name):
        request_msg = {
            "name": name
        }

        s = threading.Semaphore(0)

        def callback(success, values):
            s.release()

        self._load_controller_service_client.request(request_msg, callback)
        s.acquire()

    def _unload_controller(self, name):
        request_msg = {
            "name": name
        }

        s = threading.Semaphore(0)

        def callback(success, values):
            s.release()

        self._unload_controller_service_client.request(request_msg, callback)
        s.acquire()

class _BlueControlMode(Enum):
    """An Enum class for constants that specify control mode.

    Attributes:
        OFF: Blue is in gravity componesation mode and can be manually manipulated.
        POSITION: Blue can be controlled by sending joint position targets.
        POSE: Blue can be controlled by sending cartesian pose targets.
        TORQUE: Blue can be controlled by setting joint torque targets.
        GRIPPER: Blue gripper can be commanded.
    """
    OFF = 0
    POSITION = 1
    GRIPPER = 2
