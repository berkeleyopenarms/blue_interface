#!/usr/bin/env python3
from rosbridge_client import ROSBridgeClient
import time
import warnings
from enum import Enum
import numpy as np

class TrackerInterface:
    """An Python interface for optaining rostopic poses through ROSBridge."""

    def __init__(self, ip, tracker, port=9090):
        """Constructer for TrackerInterface.

        Args:
            ip (str): The Blue IP address. Defaults to 9090.
            tracker (str): The name of the tracker topic (assumed to be a PoseStamped topic)
            port (int, optional): The Websocket port number for rosbridge.
        """
        self._RBC = ROSBridgeClient(ip, port)
        # ROS Topic Names
        _ROS_TRACKER_TOPIC = "/" + tracker

        self._pose = None

        self._joint_state_subscriber = self._RBC.subscriber(_ROS_TRACKER_TOPIC, "geometry_msgs/PoseStamped", self._tracker_pose_callback)
        self._cartesian_pose_publisher = self._RBC.publisher(_ROS_POSE_TOPIC, "geometry_msgs/PoseStamped")

        while self._pose is Non:
            time.sleep(.1)

    def _tracker_pose_callback(self, message):
        pose = message["pose"]
        trans = pose["translation"]
        rot = pose["rotation"]
        cartesian_pose_temp = {}
        cartesian_pose_temp["position"] = np.array([trans["x"], trans["y"], trans["z"]])
        cartesian_pose_temp["orientation"] = np.array([rot["x"], rot["y"], rot["z"], rot["w"]])
        self._pose = cartesian_pose_temp

    def get_pose(self):
        """Get the current pose

        Returns:
            dict: Pose in the form {"position": numpy.array([x,y,z]), "orientation": numpy.array([x,y,z,w]} defined with repect to the world frame.
        """
        return self._pose

# example usage
if __name__ == "main":
    tracker = TrackerInterface("hekate.cs.berkeley.edu", "upper_arm_tracker_pose")
    current_tracker_pose = tracker.get_pose()
    print(current_tracker_pose)
