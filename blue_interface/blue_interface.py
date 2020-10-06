import atexit
import threading
import time
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence

import numpy as np

from .rosbridge_client import ROSBridgeClient


class BlueInterface:
    """A Python interface for controlling the Blue robot through rosbridge.

    Args:
        side (str): side of the arm, "left" or "right"
        ip (str): The IP address of the robot, which by default should have
            a running rosbridge server.
        port (int, optional): The websocket port number for rosbridge.
            Defaults to 9090.
    """

    def __init__(
        self,
        side,  # type: str
        ip,  # type: str
        port=9090,  # type: int
    ):  # type: (...) -> None
        assert side == "left" or side == "right"

        self._RBC = ROSBridgeClient(ip, port)

        # ROS topic names
        topic_prefix = "/" + side + "_arm/"
        ROS_POSITION_TOPIC = (
            topic_prefix + "blue_controllers/joint_position_controller/command"
        )
        ROS_SOFT_POSITION_TOPIC = (
            topic_prefix + "blue_controllers/joint_soft_position_controller/command"
        )
        ROS_TORQUE_TOPIC = (
            topic_prefix + "blue_controllers/joint_torque_controller/command"
        )
        ROS_JOINT_STATE_TOPIC = "/joint_states"
        ROS_GRIPPER_TOPIC = (
            topic_prefix + "blue_controllers/gripper_controller/gripper_cmd"
        )

        # Frame names
        self._WORLD_FRAME = "base_link"
        self._END_EFFECTOR_FRAME = side + "_gripper_finger_link"

        # Joint names
        self._joint_names = [
            "{}_{}".format(side, j)
            for j in [
                "base_roll_joint",
                "shoulder_lift_joint",
                "shoulder_roll_joint",
                "elbow_lift_joint",
                "elbow_roll_joint",
                "wrist_lift_joint",
                "wrist_roll_joint",
            ]
        ]
        self._gripper_joint_name = side + "_gripper_joint"

        # Controller names
        self._controller_lookup = {
            _BlueController.GRAV_COMP: "",
            _BlueController.POSITION: "blue_controllers/joint_position_controller",
            _BlueController.SOFT_POSITION: "blue_controllers/joint_soft_position_controller",
            _BlueController.GRIPPER: "blue_controllers/gripper_controller",
            _BlueController.TORQUE: "blue_controllers/joint_torque_controller",
        }

        # Robot state values! These will be populated later
        self._joint_positions = None  # type: Optional[np.ndarray]
        self._cartesian_pose = None  # type: Optional[Dict[str, np.ndarray]]
        self._joint_torques = None  # type: Optional[np.ndarray]
        self._joint_velocities = None  # type: Optional[np.ndarray]
        self._gripper_goal_id = None  # type: Optional[int]
        self._gripper_position = None  # type: Optional[float]
        self._gripper_effort = None  # type: Optional[float]

        # Joint state pub/sub
        self._joint_state_subscriber = self._RBC.subscriber(
            ROS_JOINT_STATE_TOPIC, "sensor_msgs/JointState", self._joint_state_callback
        )
        self._joint_position_publisher = self._RBC.publisher(
            ROS_POSITION_TOPIC, "std_msgs/Float64MultiArray"
        )
        self._joint_soft_position_publisher = self._RBC.publisher(
            ROS_SOFT_POSITION_TOPIC, "std_msgs/Float64MultiArray"
        )
        self._joint_torque_publisher = self._RBC.publisher(
            ROS_TORQUE_TOPIC, "std_msgs/Float64MultiArray"
        )

        # Controller manager services
        self._switch_controller_service_client = self._RBC.service(
            topic_prefix + "controller_manager/switch_controller",
            "controller_manager_msgs/SwitchController",
        )
        self._load_controller_service_client = self._RBC.service(
            topic_prefix + "controller_manager/load_controller",
            "controller_manager_msgs/LoadController",
        )
        self._unload_controller_service_client = self._RBC.service(
            topic_prefix + "controller_manager/unload_controller",
            "controller_manager_msgs/UnloadController",
        )

        # Inverse kinematics service
        self._inverse_kinematics_client = self._RBC.service(
            topic_prefix + "inverse_kinematics", "blue_msgs/InverseKinematics"
        )

        # Gripper calibration service
        self._calibrate_gripper_client = self._RBC.service(
            topic_prefix + "calibrate_gripper", "std_srvs/Trigger"
        )

        # TF repub service
        self._tf_service_client = self._RBC.service(
            "/republish_tfs", "tf2_web_republisher/RepublishTFs"
        )

        # Gripper action client
        self._gripper_action_client = self._RBC.action_client(
            ROS_GRIPPER_TOPIC, "control_msgs/GripperCommandAction"
        )

        # Start listening to world->end effector transforms
        self._request_end_effector_tfs()

        # Cleaner exiting
        atexit.register(self.shutdown)

        # Load controllers
        self._load_controller(self._controller_lookup[_BlueController.POSITION])
        self._load_controller(self._controller_lookup[_BlueController.SOFT_POSITION])
        self._load_controller(self._controller_lookup[_BlueController.GRIPPER])
        self._load_controller(self._controller_lookup[_BlueController.TORQUE])

        # Make controllers are stopped
        self._switch_controller(
            [],
            [
                self._controller_lookup[_BlueController.POSITION],
                self._controller_lookup[_BlueController.SOFT_POSITION],
                self._controller_lookup[_BlueController.GRIPPER],
                self._controller_lookup[_BlueController.TORQUE],
            ],
        )
        self._control_mode = _BlueController.GRAV_COMP
        self._gripper_enabled = False

        while self._cartesian_pose is None or self._joint_positions is None:
            time.sleep(0.1)

    def shutdown(self):  # type: (...) -> None
        """Clean up and close connection to host computer. All control will be
        disabled. This can be called manually, but will also run automatically
        when your script exits."""

        self._switch_controller(
            [],
            [
                self._controller_lookup[_BlueController.POSITION],
                self._controller_lookup[_BlueController.SOFT_POSITION],
                self._controller_lookup[_BlueController.GRIPPER],
                self._controller_lookup[_BlueController.TORQUE],
            ],
        )
        self._unload_controller(self._controller_lookup[_BlueController.POSITION])
        self._unload_controller(self._controller_lookup[_BlueController.SOFT_POSITION])
        self._unload_controller(self._controller_lookup[_BlueController.GRIPPER])
        self._unload_controller(self._controller_lookup[_BlueController.TORQUE])
        self._RBC.close()

    def calibrate_gripper(self):  # type: (...) -> None
        """Run the gripper position calibration process.
        This will automatically determine the gripper position by apply a closing
        torque and detecting when the gripper has fully closed."""

        gripper_enabled = self._gripper_enabled
        if gripper_enabled:
            self.disable_gripper()

        s = threading.Semaphore(0)

        def callback(success, values):
            s.release()

        self._calibrate_gripper_client.request({}, callback)
        s.acquire()

        if gripper_enabled:
            self.enable_gripper()

    def command_gripper(
        self,
        position,  # type: float
        effort,  # type: float
        wait=False,  # type: bool
    ):  # type: (...) -> None
        """Send a goal to gripper, and optionally wait for the goal to be reached.

        Args:
            position (float64): gap size between gripper fingers in cm.
            effort (float64): maximum effort the gripper with exert before
                stalling in N.
        """
        # TODO: change robot-side so position and effort in correct units

        if not self._gripper_enabled:
            self.enable_gripper()

        goal_msg = {"command": {"position": position, "max_effort": effort}}

        s = threading.Semaphore(0)

        def callback(result, status):
            if result["stalled"] or result["reached_goal"]:
                s.release()

        self._gripper_goal_id = self._gripper_action_client.send_goal(
            goal_msg, callback, callback
        )
        if wait:
            s.acquire()

    def cancel_gripper_command(self):  # type: (...) -> None
        """Cancel current gripper command, halting gripper in current position."""
        self._gripper_action_client.cancel_goal(self._gripper_goal_id)

    def get_gripper_position(self):  # type: (...) -> float
        """Get the current gap between gripper fingers.

        Returns:
            float64: the gripper gap in cm.

        """
        assert self._gripper_position is not None, "Gripper position not yet populated!"
        return self._gripper_position

    def get_gripper_effort(self):  # type: (...) -> float
        """Get the current effort exerted by the gripper.

        Returns:
            float64: the gripper effort in N
        """
        assert self._gripper_effort is not None, "Gripper effort not yet populated!"
        return self._gripper_effort

    def set_joint_positions(
        self,
        joint_positions,  # type: Sequence
        duration=0.0,  # type: float
        soft_position_control=False,  # type: bool
    ):  # type: (...) -> None
        """Move arm to specified position in joint space.

        Args:
            joint_positions (iterable): An array of 7 joint angles, in radians,
                ordered from proximal to distal.
            duration (float, optional): Seconds to take to reach the target,
                interpolating in joint space. Defaults to 0.
            soft_position_control (bool, optional): Use "software" position
                control, which runs position control loop at the ROS-level,
                rather than on the motor drivers. This should be rarely needed.
                Defaults to False.
        """
        joint_positions = np.asarray(joint_positions)
        assert len(joint_positions) == 7

        self._set_control_mode(
            _BlueController.SOFT_POSITION
            if soft_position_control
            else _BlueController.POSITION
        )

        start_positions = self.get_joint_positions()
        start_time = time.time()
        end_time = start_time + duration
        while time.time() < end_time:
            scale = (time.time() - start_time) / duration
            self._set_joint_positions(
                start_positions + scale * (joint_positions - start_positions),
                soft_position_control,
            )
            time.sleep(1.0 / 60.0)

        self._set_joint_positions(joint_positions, soft_position_control)

    def _set_joint_positions(
        self,
        joint_positions,  # type: Sequence
        soft_position_control,  # type: bool
    ):  # type: (...) -> None
        joint_positions_msg = {"layout": {}, "data": list(joint_positions)}
        if soft_position_control:
            self._joint_soft_position_publisher.publish(joint_positions_msg)
        else:
            self._joint_position_publisher.publish(joint_positions_msg)

    def set_joint_torques(
        self, joint_torques  # type: Sequence
    ):  # type: (...) -> None
        """Command joint torques to the arm.

        Args:
            joint_torques (iterable): An array of 7 joint torques, in Nm,
            ordered from proximal to distal.
        """

        joint_torques = list(joint_torques)
        assert len(joint_torques) == 7

        self._set_control_mode(_BlueController.TORQUE)

        joint_torques_msg = {"layout": {}, "data": list(joint_torques)}
        self._joint_torque_publisher.publish(joint_torques_msg)

    def get_joint_positions(self):  # type: (...) -> np.ndarray
        """Get the current joint angles, in radians.

        Returns:
            numpy.ndarray: An array of 7 angles, in radians, ordered from
            proximal to distal.
        """
        assert self._joint_positions is not None, "Joint positions not populated!"
        return self._joint_positions

    def get_cartesian_pose(self):  # type: (...) -> Dict[str, np.ndarray]
        """Get the current cartesian pose of the end effector, with respect to
        the world frame.

        Returns:
            dict: Pose in the form {"position": numpy.array([x,y,z]),
            "orientation": numpy.array([x,y,z,w]} defined with respect to the
            world frame.
        """
        assert self._cartesian_pose is not None, "Cartesian pose not populated!"
        return self._cartesian_pose

    def get_joint_torques(self):  # type: (...) -> np.ndarray
        """Get the current joint torques.

        Returns:
            numpy.ndarray: An array of 7 joint torques, in Nm, ordered from
            proximal to distal.
        """
        assert self._joint_torques is not None, "Joint torques not populated!"
        return self._joint_torques

    def get_joint_velocities(self):  # type: (...) -> np.ndarray
        """Get the current joint velocities.

        Returns:
            numpy.ndarray: An array of 7 joint torques, in Nm, ordered from
            proximal to distal.
        """
        assert self._joint_velocities is not None, "Joint velocities not populated!"
        return self._joint_velocities

    def disable_control(self):  # type: (...) -> None
        """Set joint control mode to gravity compensation only."""
        self._set_control_mode(_BlueController.GRAV_COMP)

    def enable_gripper(self):  # type: (...) -> None
        """Enables the gripper. The gripper will begin to hold position."""
        self._switch_controller([self._controller_lookup[_BlueController.GRIPPER]], [])
        self._gripper_enabled = True

    def disable_gripper(self):  # type: (...) -> None
        """Disables the gripper. The gripper will become compliant."""
        self._switch_controller([], [self._controller_lookup[_BlueController.GRIPPER]])
        self._gripper_enabled = False

    def gripper_enabled(self):  # type: (...) -> bool
        """Check if gripper is enabled to take commands.

        Returns:
            bool: True if enabled, False otherwise.
        """
        return self._gripper_enabled

    def inverse_kinematics(
        self,
        position,  # type: np.ndarray
        orientation,  # type: np.ndarray
        seed_joint_positions=[],  # type: Sequence
    ):  # type: (...) -> np.ndarray
        """Given a desired cartesian pose for the end effector, compute the
        necessary joint angles. Note that the system is underparameterized and
        there are an infinite number of possible solutions; this will only
        return a single possible one.

        Args:
            position (iterable): A length-3 array containing a cartesian position
                (x,y,z), wrt the world frame.
            orientation (iterable): A length-4 array containing a quaternion
                (x,y,z,w), wrt the world frame.
            seed_joint_positions (iterable, optional): An array of 7 joint
                angles, to be used to initalize the IK solver.
        Returns:
            numpy.ndarray: An array of 7 joint angles, or an empty array if no
            solution was found.
        """

        output = []
        s = threading.Semaphore(0)

        def callback(success, values):
            if success:
                output.extend(values["ik_joint_positions"])
            s.release()

        request_msg = {
            "end_effector_pose": {
                "header": {"frame_id": self._WORLD_FRAME},
                "pose": {
                    "position": dict(zip("xyz", position)),
                    "orientation": dict(zip("xyzw", orientation)),
                },
            },
            "solver": "trac-ik",
            "seed_joint_positions": seed_joint_positions,
        }
        self._inverse_kinematics_client.request(request_msg, callback)
        s.acquire()

        return np.asarray(output)

    def _joint_state_callback(
        self, message  # type: Dict[str, Any]
    ):  # type: (...) -> None
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
            index = message["name"].index(self._gripper_joint_name)
            self._gripper_position = message["position"][index]
            self._gripper_effort = message["effort"][index]

        if len(joint_positions_temp) != 0:
            self._joint_positions = np.array(joint_positions_temp)
        if len(joint_torques_temp) != 0:
            self._joint_torques = np.array(joint_torques_temp)
        if len(joint_velocities_temp) != 0:
            self._joint_velocities = np.array(joint_velocities_temp)

    def _process_tfs(
        self, message  # type: Dict[str, Any]
    ):  # type: (...) -> None
        pose = message["transforms"][0]["transform"]
        trans = pose["translation"]
        rot = pose["rotation"]
        cartesian_pose_temp = {}
        cartesian_pose_temp["position"] = np.array([trans["x"], trans["y"], trans["z"]])
        cartesian_pose_temp["orientation"] = np.array(
            [rot["x"], rot["y"], rot["z"], rot["w"]]
        )
        self._cartesian_pose = cartesian_pose_temp

    def _request_end_effector_tfs(self):  # type: (...) -> None
        goal_msg = {
            "source_frames": [self._END_EFFECTOR_FRAME],
            "target_frame": self._WORLD_FRAME,
            "angular_thres": 0,
            "trans_thres": 0,
            "rate": 30,
            "timeout": {"secs": 2.0, "nsecs": 0.0},
        }

        def _tf_service_callback(success, values):
            if success:
                self._tf_subscriber = self._RBC.subscriber(
                    values["topic_name"],
                    "tf2_web_republisher/TFArray",
                    self._process_tfs,
                )

        self._tf_service_client.request(goal_msg, _tf_service_callback)

    def _set_control_mode(
        self, mode  # type: _BlueController
    ):  # type: (...) -> bool
        if mode == self._control_mode:
            return True
        self._switch_controller(
            [self._controller_lookup[mode]],
            [self._controller_lookup[self._control_mode]],
            new_control_mode=mode,
        )
        return mode == self._control_mode

    def _switch_controller(
        self,
        start,  # type: List[str]
        stop,  # type: List[str]
        new_control_mode=None,  # type: Optional[_BlueController]
    ):  # type: (...) -> None
        request_msg = {
            "start_controllers": start,
            "stop_controllers": stop,
            "strictness": 1,  # best effort
        }

        s = threading.Semaphore(0)

        def callback(success, values):
            if success and new_control_mode is not None:
                self._control_mode = new_control_mode
            s.release()

        self._switch_controller_service_client.request(request_msg, callback)
        s.acquire()

        # Even after the controller is successfully switched, it needs a moment
        # to instantiate the command topic subscriber, etc
        time.sleep(0.01)

    def _load_controller(
        self, name  # type: str
    ):  # type: (...) -> None
        request_msg = {"name": name}

        s = threading.Semaphore(0)

        def callback(success, values):
            s.release()

        self._load_controller_service_client.request(request_msg, callback)
        s.acquire()

    def _unload_controller(
        self, name  # type: str
    ):  # type: (...) -> None
        request_msg = {"name": name}

        s = threading.Semaphore(0)

        def callback(success, values):
            s.release()

        self._unload_controller_service_client.request(request_msg, callback)
        s.acquire()


class _BlueController(Enum):
    """Enum for specifying Blue controller types.
    Note that GRAV_COMP, POSITION, and TORQUE are mutually exclusive.

    Attributes:
        GRAV_COMP: No joint control; pure gravity compensation
        POSITION: Joint position controller
        SOFT_POSITION: "Soft" joint position controller
                       This runs control at the ROS-level at ~140Hz
                       instead of on the motor drivers at ~20kHz --
                       control is worse but allows gains to be tuned
                       dynamically
        TORQUE: Joint torque controller
        GRIPPER: Gripper controller
    """

    GRAV_COMP = 0
    POSITION = 1
    SOFT_POSITION = 2
    TORQUE = 3
    GRIPPER = 4
