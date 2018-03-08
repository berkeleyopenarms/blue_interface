<h1 id="koko_interface.KokoInterface">KokoInterface</h1>

```python
KokoInterface(self, ip, port=9090)
```

<h2 id="koko_interface.KokoInterface.set_cartesian_pose">set_cartesian_pose</h2>

```python
KokoInterface.set_cartesian_pose(self, position, orientation)
```

Moves end effector to specified pose in Cartesian space.

@param position: a numpy array containing Cartesian coordinates (x,y,z) in the base_link frame
@param orientation: a numpy array containing a quaternion (x,y,z,w) defined in the base_link frame

<h2 id="koko_interface.KokoInterface.set_control_mode">set_control_mode</h2>

```python
KokoInterface.set_control_mode(self, mode)
```

Allows user to switch between available control modes.

@param mode: a KokoControlMode member -- CONTROL_OFF, JOINT_POSITIONS, or CARTESIAN_POSE
@return: a boolean that indicates success in setting the control mode

<h2 id="koko_interface.KokoInterface.get_joint_positions">get_joint_positions</h2>

```python
KokoInterface.get_joint_positions(self)
```

Returns the current position of the arm in joint space.

@return: a list of 7 angles, in radians, ordered from proximal to distal

<h2 id="koko_interface.KokoInterface.set_joint_positions">set_joint_positions</h2>

```python
KokoInterface.set_joint_positions(self, joint_positions)
```

Moves arm to specified positions in joint space.

@param joint_positions: a numpy array  of 7 joint angles, in radians, ordered from proximal to distal

