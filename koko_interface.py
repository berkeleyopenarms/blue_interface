#!/usr/bin/env python3
from rosbridge_client import ROSBridgeClient
import csv
import numpy
import time
import sys


class KokoInterface:
    """ a class to control a Koko"""

    def __init__(self, ip, port=9090, buffer_size=4096):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.RBC = ROSBridgeClient(ip)

        """ ROS Topic Names """
        _ROS_SET_JOINT_ANGLES_TOPIC = '/koko_controllers/joint_position_controller/command'
        _ROS_GET_JOINT_ANGLES_TOPIC = '/joint_states'
        _ROS_SET_CARTESIAN_POSE_TOPIC = ' '
        _ROS_GET_CARTESIAN_POSE_TOPIC = ''
        _ROS_SET_P_TERMS_TOPIC = '/p_terms'
        _ROS_SET_D_TERMS_TOPIC = '/d_terms'

        """ Create Subscribers and Publishers """
        self._joint_angles_subscriber = self.RBC.subscriber(_ROS_GET_JOINT_ANGLES_TOPIC, "sensor_msgs/JointState", self._joint_angles_callback)
        self._joint_angles_publisher = self.RBC.publisher(_ROS_SET_JOINT_ANGLES_TOPIC, "std_msgs/Float64MultiArray")
        self._cartesian_pose_subscriber = self.RBC.subscriber(_ROS_SET_CARTESIAN_POSE_TOPIC, "geometry_msgs/PoseStamped")
        self._cartesian_pose_publisher = self.RBC.publisher(_ROS_GET_CARTESIAN_POSE_TOPIC, "geometry_msgs/PoseStamped")
        self._p_terms_publisher = self.RBC.publisher(_ROS_SET_P_TERMS_TOPIC, "std_msgs/Float64MultiArray")
        self._d_terms_publisher = self.RBC.publisher(_ROS_SET_D_TERMS_TOPIC, "std_msgs/Float64MultiArray")

        self.is_debug = False
        self.joint_angles = None
        self.cartesian_pose = None
        self.joint_names = ['base_roll_joint', 'shoulder_lift_joint', 'shoulder_roll_joint', 'elbow_lift_joint', 'elbow_roll_joint', 'wrist_lift_joint', 'wrist_roll_joint']

    def _joint_angles_callback(self, message):
        joint_angles_temp = []
        for name in self.joint_names:
            self.index = message['name'].index(name)
            joint_angles_temp.append(message['position'][self.index])
        self.joint_angles = joint_angles_temp

    def set_joint_angle_target(self, joint_angles):
        """ joint_positions is a list of 7 angles, in rads, from proximal to distal """
        joint_angles_message = {
            "layout" : {},
            "data": joint_angles
        }
        self._joint_angles_publisher.publish(joint_angles_message)
        while self.is_debug:
            self._joint_angles_publisher.publish(joint_angles_message)

    def set_cartesian_pose_target(self, position, orientation):
        position_message = {
            "x": position[0]
            "y": position[1]
            "z": position[2]
        }
        orientation message = {
            "x": orientation[0]
            "y": orientation[1]
            "z": orientation[2]
            "w": orientation[3]
        }
        pose_message = {
            "position": position_message
            "orientation": orientation_message
        }
        cartesian_pose_message = {
            "header": {}
            "pose" = pose_message
        }
        self.set_cartesian_pose_publisher.publish(cartesian_pose_message)

    def get_joint_angles(self):
        if self.is_debug:
            print(self.joint_angles)
        return self.joint_angles

    def _pd_off(self):
        p_terms_message = {
            "layout" : {},
            "data": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        }
        d_terms_message = {
            "layout" : {},
            "data": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        }
        self._p_terms_publisher.publish(p_terms_message)
        self._d_terms_publisher.publish(d_terms_message)

    def _pd_on(self):
        p_terms_message = {
            "layout" : {},
            "data": [12.0, 12.0, 12.0, 5.0, 5.0, 3.0, 3.0]
        }
        d_terms_message = {
            "layout" : {},
            "data": [3.0, 4.0, 3.0, 2.0, 2.0, 1.0, 1.0]
        }
        self._p_terms_publisher.publish(p_terms_message)
        self._d_terms_publisher.publish(d_terms_message)

if __name__== '__main__':
    koko = KokoInterface('hekate.cs.berkeley.edu')
    koko.set_joint_angle_target([0,0,0,0,0,0,0])
    time.sleep(1)
    koko.get_joint_angles()
