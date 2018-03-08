#### `get_control_mode()`


_joint_positions_callback(self, message):
joint_positions_temp = []
for name in self._joint_names:
self.index = message["name"].index(name)
joint_positions_temp.append(message["position"][self.index])
self.joint_positions = joint_positions_temp

_process_tfs(self, message):
print(message)

_call_tf_service(self):
goal_msg = {
"source_frames": [self._END_EFFECTOR_FRAME],
"target_frame": self._WORLD_FRAME,
"angular_thres": 0.0,
"trans_thres": 0.0,
"rate": 10.0,
"timeout": 200.0
}

def _tf_service_callback(success, values):
if success:
    self._tf_subscriber = self._RBC.subscriber(values["topic_name"], "geometry_msgs/TransformStamped[]", self._process_tfs)
    print(values["topic_name"])

self._tf_service_client.request(goal_msg, _tf_service_callback)

koControlMode(Enum):
DO add torque control mode
ROL_OFF = 0
T_POSITIONS = 1
ESIAN_POSE = 2


#### `get_joint_positions()`

Returns the current position of the arm in joint space.

@return: a list of 7 angles, in radians, ordered from proximal to distal

#### `set_cartesian_pose(position, orientation)`

Moves end effector to specified pose in Cartesian space.

@param position: a numpy array containing Cartesian coordinates (x,y,z) in the base_link frame
@param orientation: a numpy array containing a quaternion (x,y,z,w) defined in the base_link frame

#### `set_control_mode(mode)`


#### `set_joint_positions(joint_positions)`

Moves arm to specified positions in joint space.

@param joint_positions: a numpy array  of 7 joint angles, in radians, ordered from proximal to distal