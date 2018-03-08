Help on module koko_interface:

NAME
    koko_interface

FILE
    /home/brent/koko_interface/koko_interface.py

CLASSES
    enum.Enum(__builtin__.object)
        KokoControlMode
    KokoInterface
    
    KokoControlMode = <enum 'KokoControlMode'>
    class KokoInterface
     |  Methods defined here:
     |  
     |  __init__(self, ip, port=9090)
     |  
     |  get_control_mode(self)
     |  
     |  get_joint_positions(self)
     |      Returns the current position of the arm in joint space.
     |      
     |      @return: a list of 7 angles, in radians, ordered from proximal to distal
     |  
     |  set_cartesian_pose(self, position, orientation)
     |      Moves end effector to specified pose in Cartesian space.
     |      
     |      @param position: a numpy array containing Cartesian coordinates (x,y,z) in the base_link frame
     |      @param orientation: a numpy array containing a quaternion (x,y,z,w) defined in the base_link frame
     |  
     |  set_control_mode(self, mode)
     |      Allows user to switch between available control modes.
     |      
     |      @param mode: a KokoControlMode member -- CONTROL_OFF, JOINT_POSITIONS, or CARTESIAN_POSE
     |      @return: a boolean that indicates success in setting the control mode
     |  
     |  set_joint_positions(self, joint_positions)
     |      Moves arm to specified positions in joint space.
     |      
     |      @param joint_positions: a numpy array  of 7 joint angles, in radians, ordered from proximal to distal


