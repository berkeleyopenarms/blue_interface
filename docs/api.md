# Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`namespace `[`koko_interface`](#namespacekoko__interface) | 
`namespace `[`rosbridge_client`](#namespacerosbridge__client) | 
`namespace `[`tf_client`](#namespacetf__client) | 

# namespace `koko_interface` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`koko_interface::KokoControlMode`](#classkoko__interface_1_1KokoControlMode) | 
`class `[`koko_interface::KokoInterface`](#classkoko__interface_1_1KokoInterface) | 

# class `koko_interface::KokoControlMode` 

```
class koko_interface::KokoControlMode
  : public Enum
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------

## Members

# class `koko_interface::KokoInterface` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`joint_positions`](#classkoko__interface_1_1KokoInterface_1a28d2873e3b1fcdc4f606a07cbf81d210) | 
`public  `[`cartesian_pose`](#classkoko__interface_1_1KokoInterface_1a30ad900674c0c86e1591b319cec4a6c0) | 
`public  `[`control_mode`](#classkoko__interface_1_1KokoInterface_1a574b916f7eef570c7a02df84bd1c7b19) | 
`public  `[`index`](#classkoko__interface_1_1KokoInterface_1a188c53b5a1fa6d13f4056320017c9d29) | 
`public def `[`__init__`](#classkoko__interface_1_1KokoInterface_1aaf543c0820da6c38ee61d423d995da0b)`(self,ip,port)` | 
`public def `[`set_joint_positions`](#classkoko__interface_1_1KokoInterface_1a8001867f243714800f78a34b54d44421)`(self,joint_positions)` | Moves arm to specified positions in joint space.
`public def `[`set_cartesian_pose`](#classkoko__interface_1_1KokoInterface_1a11cf37925d4d98477a95734704e1c958)`(self,position,orientation)` | Moves end effector to specified pose in Cartesian space.
`public def `[`get_joint_positions`](#classkoko__interface_1_1KokoInterface_1aef18bb753953d1d47a1225fe19bf5ef1)`(self)` | Returns the current position of the arm in joint space.
`public def `[`set_control_mode`](#classkoko__interface_1_1KokoInterface_1a27bbfb3dbb835d72674ecfaec6b26c03)`(self,mode)` | Allows user to switch between available control modes.
`public def `[`get_control_mode`](#classkoko__interface_1_1KokoInterface_1ab15cbe6d263b88ccfd667f16b43bef83)`(self)` | 

## Members

#### `public  `[`joint_positions`](#classkoko__interface_1_1KokoInterface_1a28d2873e3b1fcdc4f606a07cbf81d210) 

#### `public  `[`cartesian_pose`](#classkoko__interface_1_1KokoInterface_1a30ad900674c0c86e1591b319cec4a6c0) 

#### `public  `[`control_mode`](#classkoko__interface_1_1KokoInterface_1a574b916f7eef570c7a02df84bd1c7b19) 

#### `public  `[`index`](#classkoko__interface_1_1KokoInterface_1a188c53b5a1fa6d13f4056320017c9d29) 

#### `public def `[`__init__`](#classkoko__interface_1_1KokoInterface_1aaf543c0820da6c38ee61d423d995da0b)`(self,ip,port)` 

#### `public def `[`set_joint_positions`](#classkoko__interface_1_1KokoInterface_1a8001867f243714800f78a34b54d44421)`(self,joint_positions)` 

Moves arm to specified positions in joint space.

#### Parameters
* `joint_positions` a numpy array of 7 joint angles, in radians, ordered from proximal to distal

#### `public def `[`set_cartesian_pose`](#classkoko__interface_1_1KokoInterface_1a11cf37925d4d98477a95734704e1c958)`(self,position,orientation)` 

Moves end effector to specified pose in Cartesian space.

#### Parameters
* `position` a numpy array containing Cartesian coordinates (x,y,z) in the base_link frame 

* `orientation` a numpy array containing a quaternion (x,y,z,w) defined in the base_link frame

#### `public def `[`get_joint_positions`](#classkoko__interface_1_1KokoInterface_1aef18bb753953d1d47a1225fe19bf5ef1)`(self)` 

Returns the current position of the arm in joint space.

#### Returns
: a list of 7 angles, in radians, ordered from proximal to distal

#### `public def `[`set_control_mode`](#classkoko__interface_1_1KokoInterface_1a27bbfb3dbb835d72674ecfaec6b26c03)`(self,mode)` 

Allows user to switch between available control modes.

#### Parameters
* `mode` a [KokoControlMode](#classkoko__interface_1_1KokoControlMode) member  CONTROL_OFF, JOINT_POSITIONS, or CARTESIAN_POSE 

#### Returns
: a boolean that indicates success in setting the control mode

#### `public def `[`get_control_mode`](#classkoko__interface_1_1KokoInterface_1ab15cbe6d263b88ccfd667f16b43bef83)`(self)` 

# namespace `rosbridge_client` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`rosbridge_client::_ActionClient`](#classrosbridge__client_1_1__ActionClient) | 
`class `[`rosbridge_client::_Goal`](#classrosbridge__client_1_1__Goal) | 
`class `[`rosbridge_client::_Publisher`](#classrosbridge__client_1_1__Publisher) | 
`class `[`rosbridge_client::_Service`](#classrosbridge__client_1_1__Service) | 
`class `[`rosbridge_client::_Subscriber`](#classrosbridge__client_1_1__Subscriber) | 
`class `[`rosbridge_client::ROSBridgeClient`](#classrosbridge__client_1_1ROSBridgeClient) | [ROSBridgeClient](#classrosbridge__client_1_1ROSBridgeClient) extends WebSocketClient and manages connection to the server and all interactions with ROS.

# class `rosbridge_client::_ActionClient` 

```
class rosbridge_client::_ActionClient
  : public object
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`__init__`](#classrosbridge__client_1_1__ActionClient_1a79b86d9a4c6909ecfc44b7ffbd091354)`(self,rosbridge,server_name,action_name)` | Constructor for [_ActionClient](#classrosbridge__client_1_1__ActionClient).
`public def `[`usage`](#classrosbridge__client_1_1__ActionClient_1aba8927b675dc635076f97110b5cf401e)`(self)` | 
`public def `[`usage`](#classrosbridge__client_1_1__ActionClient_1a362dae5630bcbf22b39984797c28b0db)`(self,value)` | 
`public def `[`on_feedback`](#classrosbridge__client_1_1__ActionClient_1adbf822ca30fcae15faf0ad080f0c6be2)`(self,message)` | Callback when a feedback message received.
`public def `[`on_result`](#classrosbridge__client_1_1__ActionClient_1ada532b56ed3d4a383212b0e54670545f)`(self,message)` | Callback when a result message received.
`public def `[`send_goal`](#classrosbridge__client_1_1__ActionClient_1a29788da4893bfbd67cba894116efbeae)`(self,goal_message,`[`on_result`](#classrosbridge__client_1_1__ActionClient_1ada532b56ed3d4a383212b0e54670545f)`,`[`on_feedback`](#classrosbridge__client_1_1__ActionClient_1adbf822ca30fcae15faf0ad080f0c6be2)`)` | Send a goal to the ROS action server.
`public def `[`cancel_goal`](#classrosbridge__client_1_1__ActionClient_1a55f112c7417133d35b6078d3bb6710fe)`(self,goal_id)` | Cancel a goal with a given goal ID.
`public def `[`unregister`](#classrosbridge__client_1_1__ActionClient_1a8b94079cddbb7573800f05adf14de56f)`(self)` | Reduce the usage of the action client.

## Members

#### `public def `[`__init__`](#classrosbridge__client_1_1__ActionClient_1a79b86d9a4c6909ecfc44b7ffbd091354)`(self,rosbridge,server_name,action_name)` 

Constructor for [_ActionClient](#classrosbridge__client_1_1__ActionClient).

#### Parameters
* `rosbridge` The [ROSBridgeClient](#classrosbridge__client_1_1ROSBridgeClient) object. 

* `server_name` The ROS action server name. 

* `action_name` The ROS action name.

#### `public def `[`usage`](#classrosbridge__client_1_1__ActionClient_1aba8927b675dc635076f97110b5cf401e)`(self)` 

#### `public def `[`usage`](#classrosbridge__client_1_1__ActionClient_1a362dae5630bcbf22b39984797c28b0db)`(self,value)` 

#### `public def `[`on_feedback`](#classrosbridge__client_1_1__ActionClient_1adbf822ca30fcae15faf0ad080f0c6be2)`(self,message)` 

Callback when a feedback message received.

#### Parameters
* `message` A feedback message received from ROS action server.

#### `public def `[`on_result`](#classrosbridge__client_1_1__ActionClient_1ada532b56ed3d4a383212b0e54670545f)`(self,message)` 

Callback when a result message received.

#### Parameters
* `message` A result message received from ROS action server.

#### `public def `[`send_goal`](#classrosbridge__client_1_1__ActionClient_1a29788da4893bfbd67cba894116efbeae)`(self,goal_message,`[`on_result`](#classrosbridge__client_1_1__ActionClient_1ada532b56ed3d4a383212b0e54670545f)`,`[`on_feedback`](#classrosbridge__client_1_1__ActionClient_1adbf822ca30fcae15faf0ad080f0c6be2)`)` 

Send a goal to the ROS action server.

#### Parameters
* `goal_message` A message to send to ROS action server. 

* `on_result` A callback function to be called when a feedback message received. 

* `on_feedback` A callback function to be called when a result message received.

#### `public def `[`cancel_goal`](#classrosbridge__client_1_1__ActionClient_1a55f112c7417133d35b6078d3bb6710fe)`(self,goal_id)` 

Cancel a goal with a given goal ID.

#### Parameters
* `goal_id` The ID of the goal to be cancelled.

#### `public def `[`unregister`](#classrosbridge__client_1_1__ActionClient_1a8b94079cddbb7573800f05adf14de56f)`(self)` 

Reduce the usage of the action client.

If the usage is 0, unregister its publishers and subscribers.

# class `rosbridge_client::_Goal` 

```
class rosbridge_client::_Goal
  : public object
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`__init__`](#classrosbridge__client_1_1__Goal_1ac92f5e42a4cd74bcede2ec41844e19ee)`(self,`[`message`](#classrosbridge__client_1_1__Goal_1a70ba894b0982d8bf9c67710d9da70d58)`,on_result,on_feedback)` | Constructor for [_Goal](#classrosbridge__client_1_1__Goal).
`public def `[`id`](#classrosbridge__client_1_1__Goal_1a462c118edcb84b9c2fca442cb6a85e58)`(self)` | 
`public def `[`message`](#classrosbridge__client_1_1__Goal_1a70ba894b0982d8bf9c67710d9da70d58)`(self)` | Wrap message in JSON format that complies ROSBridge protocol.
`public def `[`is_finished`](#classrosbridge__client_1_1__Goal_1ad710d6d2c6d7d3e2ec60f430e15b9e37)`(self)` | 
`public def `[`result_received`](#classrosbridge__client_1_1__Goal_1ac7ca4094b89938c25be35811082b7475)`(self,result,status)` | Called when a result message is received.
`public def `[`feedback_received`](#classrosbridge__client_1_1__Goal_1ae3d71a24dee5fb59d52afa53e6fc31d5)`(self,feedback,status)` | Called when a result message is received.

## Members

#### `public def `[`__init__`](#classrosbridge__client_1_1__Goal_1ac92f5e42a4cd74bcede2ec41844e19ee)`(self,`[`message`](#classrosbridge__client_1_1__Goal_1a70ba894b0982d8bf9c67710d9da70d58)`,on_result,on_feedback)` 

Constructor for [_Goal](#classrosbridge__client_1_1__Goal).

#### Parameters
* `message` The goal message to send to ROS action server. 

* `on_result` A callback function to be called when a feedback message received. 

* `on_feedback` A callback function to be called when a result message received.

#### `public def `[`id`](#classrosbridge__client_1_1__Goal_1a462c118edcb84b9c2fca442cb6a85e58)`(self)` 

#### `public def `[`message`](#classrosbridge__client_1_1__Goal_1a70ba894b0982d8bf9c67710d9da70d58)`(self)` 

Wrap message in JSON format that complies ROSBridge protocol.

#### Returns
A Json that contains the goal ID and message.

#### `public def `[`is_finished`](#classrosbridge__client_1_1__Goal_1ad710d6d2c6d7d3e2ec60f430e15b9e37)`(self)` 

#### `public def `[`result_received`](#classrosbridge__client_1_1__Goal_1ac7ca4094b89938c25be35811082b7475)`(self,result,status)` 

Called when a result message is received.

#### Parameters
* `result` The result message. 

* `status` The status code. Such as: ACTIVE = 1: The goal is currently being processed by the action server; PREEMPTED = 2: The goal received a cancel request after it started executing; SUCCEEDED = 3: The goal was achieved successfully by the action server; ABORTED = 4: The goal was aborted during execution by the action server due to some failure. For more details, refer to [http://docs.ros.org/indigo/api/actionlib_msgs/html/msg/GoalStatus.html](http://docs.ros.org/indigo/api/actionlib_msgs/html/msg/GoalStatus.html).

#### `public def `[`feedback_received`](#classrosbridge__client_1_1__Goal_1ae3d71a24dee5fb59d52afa53e6fc31d5)`(self,feedback,status)` 

Called when a result message is received.

#### Parameters
* `feedback` The feedback message. 

* `status` The status code. Such as: ACTIVE = 1: The goal is currently being processed by the action server; PREEMPTED = 2: The goal received a cancel request after it started executing; SUCCEEDED = 3: The goal was achieved successfully by the action server; ABORTED = 4: The goal was aborted during execution by the action server due to some failure. For more details, refer to [http://docs.ros.org/indigo/api/actionlib_msgs/html/msg/GoalStatus.html](http://docs.ros.org/indigo/api/actionlib_msgs/html/msg/GoalStatus.html).

# class `rosbridge_client::_Publisher` 

```
class rosbridge_client::_Publisher
  : public object
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`__init__`](#classrosbridge__client_1_1__Publisher_1aa73fbe39915557c7c500db88e9e43bb6)`(self,rosbridge,topic_name,message_type,latch,queue_size)` | Constructor for [_Publisher](#classrosbridge__client_1_1__Publisher).
`public def `[`usage`](#classrosbridge__client_1_1__Publisher_1a919603327c26d6ca9778e2dc7ddbeefc)`(self)` | 
`public def `[`usage`](#classrosbridge__client_1_1__Publisher_1a9ef7e0c6684d373433d6ec77cd4a0ea5)`(self,value)` | 
`public def `[`publish`](#classrosbridge__client_1_1__Publisher_1ab0700e489fe42d4c7585fcb7f077946b)`(self,message)` | Publish a ROS message.
`public def `[`unregister`](#classrosbridge__client_1_1__Publisher_1adc817bc6d8ceec2c45f33fb91cea9156)`(self)` | Reduce the usage of the publisher.

## Members

#### `public def `[`__init__`](#classrosbridge__client_1_1__Publisher_1aa73fbe39915557c7c500db88e9e43bb6)`(self,rosbridge,topic_name,message_type,latch,queue_size)` 

Constructor for [_Publisher](#classrosbridge__client_1_1__Publisher).

#### Parameters
* `rosbridge` The [ROSBridgeClient](#classrosbridge__client_1_1ROSBridgeClient) object. 

* `topic_name` The ROS topic name. 

* `message_type` The ROS message type, such as `std_msgs/String`. latch (bool, optional): Whether the topic is latched when publishing. Defaults to False. 

* `queue_size` The queue created at bridge side for re-publishing. Defaults to 1.

#### `public def `[`usage`](#classrosbridge__client_1_1__Publisher_1a919603327c26d6ca9778e2dc7ddbeefc)`(self)` 

#### `public def `[`usage`](#classrosbridge__client_1_1__Publisher_1a9ef7e0c6684d373433d6ec77cd4a0ea5)`(self,value)` 

#### `public def `[`publish`](#classrosbridge__client_1_1__Publisher_1ab0700e489fe42d4c7585fcb7f077946b)`(self,message)` 

Publish a ROS message.

#### Parameters
* `message` A message to send.

#### `public def `[`unregister`](#classrosbridge__client_1_1__Publisher_1adc817bc6d8ceec2c45f33fb91cea9156)`(self)` 

Reduce the usage of the publisher.

If the usage is 0, unadvertise this topic.

# class `rosbridge_client::_Service` 

```
class rosbridge_client::_Service
  : public object
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`__init__`](#classrosbridge__client_1_1__Service_1a55d6c8132adfb0d9ebf18e4b45d6c5e1)`(self,rosbridge,service_name,service_type)` | Constructor for [_Service](#classrosbridge__client_1_1__Service).
`public def `[`request`](#classrosbridge__client_1_1__Service_1a60d88b1c0d9e5def5e7802928453b451)`(self,request,cb)` | Send a request to the ROS service server.

## Members

#### `public def `[`__init__`](#classrosbridge__client_1_1__Service_1a55d6c8132adfb0d9ebf18e4b45d6c5e1)`(self,rosbridge,service_name,service_type)` 

Constructor for [_Service](#classrosbridge__client_1_1__Service).

#### Parameters
* `rosbridge` The [ROSBridgeClient](#classrosbridge__client_1_1ROSBridgeClient) object. 

* `service_name` The ROS service name. 

* `service_type` The ROS service type.

#### `public def `[`request`](#classrosbridge__client_1_1__Service_1a60d88b1c0d9e5def5e7802928453b451)`(self,request,cb)` 

Send a request to the ROS service server.

The callback function will be called when service responses.

#### Parameters
* `request` A request message to send, 

* `cb` A function will be called when the service server responses.

#### Returns

# class `rosbridge_client::_Subscriber` 

```
class rosbridge_client::_Subscriber
  : public object
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`__init__`](#classrosbridge__client_1_1__Subscriber_1ab7f1f516b3180b06e0f610f3874549c1)`(self,rosbridge,topic_name,cb)` | Constructor for [_Subscriber](#classrosbridge__client_1_1__Subscriber).
`public def `[`topic_name`](#classrosbridge__client_1_1__Subscriber_1a072cb9bcfa1a8db1f721d669206dac8c)`(self)` | 
`public def `[`unregister`](#classrosbridge__client_1_1__Subscriber_1a69094f92927d9978e1ece3ac3f277a26)`(self)` | Remove the current callback function from listening to the topic, and from the rosbridge client subscription list.

## Members

#### `public def `[`__init__`](#classrosbridge__client_1_1__Subscriber_1ab7f1f516b3180b06e0f610f3874549c1)`(self,rosbridge,topic_name,cb)` 

Constructor for [_Subscriber](#classrosbridge__client_1_1__Subscriber).

#### Parameters
* `rosbridge` The [ROSBridgeClient](#classrosbridge__client_1_1ROSBridgeClient) object. 

* `topic_name` The ROS topic name. 

* `cb` A function will be called when a message is received on that topic.

#### `public def `[`topic_name`](#classrosbridge__client_1_1__Subscriber_1a072cb9bcfa1a8db1f721d669206dac8c)`(self)` 

#### `public def `[`unregister`](#classrosbridge__client_1_1__Subscriber_1a69094f92927d9978e1ece3ac3f277a26)`(self)` 

Remove the current callback function from listening to the topic, and from the rosbridge client subscription list.

# class `rosbridge_client::ROSBridgeClient` 

```
class rosbridge_client::ROSBridgeClient
  : public WebSocketClient
```  

[ROSBridgeClient](#classrosbridge__client_1_1ROSBridgeClient) extends WebSocketClient and manages connection to the server and all interactions with ROS.

It keeps a record of all publishers, subscriber, service request callbacks and action clients.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`__init__`](#classrosbridge__client_1_1ROSBridgeClient_1a4d4bd7f7420e54f5f1018f21ca165f8f)`(self,ip,port)` | Constructor for [ROSBridgeClient](#classrosbridge__client_1_1ROSBridgeClient).
`public def `[`id_counter`](#classrosbridge__client_1_1ROSBridgeClient_1ae38cc794f42ac51f8be3989ac4fda18b)`(self)` | Generate an auto-incremental ID starts from 1.
`public def `[`publisher`](#classrosbridge__client_1_1ROSBridgeClient_1abfde5092083f35ca46d2d355a4d0addf)`(self,topic_name,message_type,latch,queue_size)` | Create a [_Publisher](#classrosbridge__client_1_1__Publisher) object if the given topic hasn't been advertised, otherwise return the existing publisher that is currently advertising the topic.
`public def `[`unregister_publisher`](#classrosbridge__client_1_1ROSBridgeClient_1aba3a71ffaa43a3be49e569bfd7132765)`(self,topic_name)` | Stop advertising on the given topic.
`public def `[`subscriber`](#classrosbridge__client_1_1ROSBridgeClient_1a5848414ef65379d8f8fdd79d59daf788)`(self,topic_name,message_type,cb)` | Create a [_Subscriber](#classrosbridge__client_1_1__Subscriber) object on a given topic with a callback function.
`public def `[`unsubscribe`](#classrosbridge__client_1_1ROSBridgeClient_1a934bed55ffd2cb06157cec98ed7d2efb)`(self,`[`subscriber`](#classrosbridge__client_1_1ROSBridgeClient_1a5848414ef65379d8f8fdd79d59daf788)`)` | Remove a callback subscriber from its topic subscription list.
`public def `[`service`](#classrosbridge__client_1_1ROSBridgeClient_1acd8c490a49fd9cd64468dfac2b9580a5)`(self,service_name,service_type)` | Create a ROS service client.
`public def `[`register_service_callback`](#classrosbridge__client_1_1ROSBridgeClient_1ab4ebda6ee5ec77c64160110bb7155928)`(self,service_id,cb)` | Register a service callback with a service request ID.
`public def `[`action_client`](#classrosbridge__client_1_1ROSBridgeClient_1ac1df1881e665ae4078ce957fdf32160b)`(self,server_name,action_name)` | Create a ROS action client if there was no client created for the action server.
`public def `[`unregister_action_client`](#classrosbridge__client_1_1ROSBridgeClient_1adbc3a76d30b6b1ad90721dce99da7253)`(self,server_name,action_name)` | Unregister the action client with server and action name.
`public def `[`opened`](#classrosbridge__client_1_1ROSBridgeClient_1a2f9d6ba51cef6f6569ed7178ddbd6a7e)`(self)` | Called when the connection to ROS established.
`public def `[`closed`](#classrosbridge__client_1_1ROSBridgeClient_1ae7563ccdf301dac0e121c67ac7b5bb29)`(self,code,reason)` | Called when the connection to ROS disconnected.
`public def `[`received_message`](#classrosbridge__client_1_1ROSBridgeClient_1a08b399d6d5818adac190fa13f1de362e)`(self,message)` | Called when message received from ROS server.
`public def `[`unhandled_error`](#classrosbridge__client_1_1ROSBridgeClient_1ac913d8903d90cd20c6ecdbee1e05edfb)`(self,error)` | Called when a socket or OS error is raised.

## Members

#### `public def `[`__init__`](#classrosbridge__client_1_1ROSBridgeClient_1a4d4bd7f7420e54f5f1018f21ca165f8f)`(self,ip,port)` 

Constructor for [ROSBridgeClient](#classrosbridge__client_1_1ROSBridgeClient).

#### Parameters
* `ip` The robot IP address. port (int, optional): The WebSocket port number for rosbridge. Defaults to 9090.

#### `public def `[`id_counter`](#classrosbridge__client_1_1ROSBridgeClient_1ae38cc794f42ac51f8be3989ac4fda18b)`(self)` 

Generate an auto-incremental ID starts from 1.

#### Returns
A auto-incremented ID.

#### `public def `[`publisher`](#classrosbridge__client_1_1ROSBridgeClient_1abfde5092083f35ca46d2d355a4d0addf)`(self,topic_name,message_type,latch,queue_size)` 

Create a [_Publisher](#classrosbridge__client_1_1__Publisher) object if the given topic hasn't been advertised, otherwise return the existing publisher that is currently advertising the topic.

#### Parameters
* `topic_name` The ROS topic name. 

* `message_type` The ROS message type, such as `std_msgs/String`. latch (bool, optional): Whether the topic is latched when publishing. Defaults to False. 

* `queue_size` The queue created at bridge side for re-publishing. Defaults to 1.

#### Returns
A [_Publisher](#classrosbridge__client_1_1__Publisher) object.

#### `public def `[`unregister_publisher`](#classrosbridge__client_1_1ROSBridgeClient_1aba3a71ffaa43a3be49e569bfd7132765)`(self,topic_name)` 

Stop advertising on the given topic.

#### Parameters
* `topic_name` The ROS topic name.

#### `public def `[`subscriber`](#classrosbridge__client_1_1ROSBridgeClient_1a5848414ef65379d8f8fdd79d59daf788)`(self,topic_name,message_type,cb)` 

Create a [_Subscriber](#classrosbridge__client_1_1__Subscriber) object on a given topic with a callback function.

If the topic hasn't been subscribed yet, subscribe the topic. Otherwise, it adds the subscriber with callback function into the topic subscription list.

#### Parameters
* `topic_name` The ROS topic name. 

* `message_type` The ROS message type, such as `std_msgs/String`. 

* `cb` A function will be called when a message is received on that topic.

#### Returns
A [_Subscriber](#classrosbridge__client_1_1__Subscriber) object.

#### `public def `[`unsubscribe`](#classrosbridge__client_1_1ROSBridgeClient_1a934bed55ffd2cb06157cec98ed7d2efb)`(self,`[`subscriber`](#classrosbridge__client_1_1ROSBridgeClient_1a5848414ef65379d8f8fdd79d59daf788)`)` 

Remove a callback subscriber from its topic subscription list.

If there is no callback subscribers in the subscription list. It will unsubscribe the topic.

#### Parameters
* `subscriber` A subscriber with callback function that listen to the topic.

#### `public def `[`service`](#classrosbridge__client_1_1ROSBridgeClient_1acd8c490a49fd9cd64468dfac2b9580a5)`(self,service_name,service_type)` 

Create a ROS service client.

#### Parameters
* `service_name` The ROS service name. 

* `service_type` The ROS service type.

#### Returns
A [_Service](#classrosbridge__client_1_1__Service) object.

#### `public def `[`register_service_callback`](#classrosbridge__client_1_1ROSBridgeClient_1ab4ebda6ee5ec77c64160110bb7155928)`(self,service_id,cb)` 

Register a service callback with a service request ID.

#### Parameters
* `service_id` The service request ID. 

* `cb` A function will be called when the service server responses.

#### `public def `[`action_client`](#classrosbridge__client_1_1ROSBridgeClient_1ac1df1881e665ae4078ce957fdf32160b)`(self,server_name,action_name)` 

Create a ROS action client if there was no client created for the action server.

Otherwise return that action client.

#### Parameters
* `server_name` The ROS action server name. 

* `action_name` The ROS action name.

#### Returns
A [_ActionClient](#classrosbridge__client_1_1__ActionClient) object.

#### `public def `[`unregister_action_client`](#classrosbridge__client_1_1ROSBridgeClient_1adbc3a76d30b6b1ad90721dce99da7253)`(self,server_name,action_name)` 

Unregister the action client with server and action name.

Remove it from the internal action client dict.

#### Parameters
* `server_name` The ROS action server name. 

* `action_name` The ROS action name.

#### `public def `[`opened`](#classrosbridge__client_1_1ROSBridgeClient_1a2f9d6ba51cef6f6569ed7178ddbd6a7e)`(self)` 

Called when the connection to ROS established.

#### `public def `[`closed`](#classrosbridge__client_1_1ROSBridgeClient_1ae7563ccdf301dac0e121c67ac7b5bb29)`(self,code,reason)` 

Called when the connection to ROS disconnected.

#### Parameters
* `code` A status code. reason (str, opitonal): A human readable message. Defaults to None.

#### `public def `[`received_message`](#classrosbridge__client_1_1ROSBridgeClient_1a08b399d6d5818adac190fa13f1de362e)`(self,message)` 

Called when message received from ROS server.

Only handle the message with `topic` or `service` keywords and trigger corresponding callback functions.

#### Parameters
* `message` A message that sent from ROS server.

#### `public def `[`unhandled_error`](#classrosbridge__client_1_1ROSBridgeClient_1ac913d8903d90cd20c6ecdbee1e05edfb)`(self,error)` 

Called when a socket or OS error is raised.

#### Parameters
* `error` A human readable error message.

# namespace `tf_client` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`tf_client::TFClient`](#classtf__client_1_1TFClient) | 

# class `tf_client::TFClient` 

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`RBC`](#classtf__client_1_1TFClient_1a5428e6d8f93c2193a22b0b04c27d873d) | 
`public  `[`tf_service_client`](#classtf__client_1_1TFClient_1a42d041cb8036ed3145c92e22d14b4921) | 
`public def `[`__init__`](#classtf__client_1_1TFClient_1a8edc8e47d671ce0b123b4c6789679394)`(self,ip,port,options)` | 
`public def `[`updateGoal`](#classtf__client_1_1TFClient_1adae0b76f2fcf0dc4a20beacd1f730af8)`()` | 
`public def `[`updateGoal_callback`](#classtf__client_1_1TFClient_1aae9c6ce7334fd4c3be7692657a48ca6e)`(self,topic_name)` | 
`public def `[`process_tf_callback`](#classtf__client_1_1TFClient_1ae4c93dbacad72dbb84ed8139442e6864)`(self,message)` | 

## Members

#### `public  `[`RBC`](#classtf__client_1_1TFClient_1a5428e6d8f93c2193a22b0b04c27d873d) 

#### `public  `[`tf_service_client`](#classtf__client_1_1TFClient_1a42d041cb8036ed3145c92e22d14b4921) 

#### `public def `[`__init__`](#classtf__client_1_1TFClient_1a8edc8e47d671ce0b123b4c6789679394)`(self,ip,port,options)` 

#### `public def `[`updateGoal`](#classtf__client_1_1TFClient_1adae0b76f2fcf0dc4a20beacd1f730af8)`()` 

#### `public def `[`updateGoal_callback`](#classtf__client_1_1TFClient_1aae9c6ce7334fd4c3be7692657a48ca6e)`(self,topic_name)` 

#### `public def `[`process_tf_callback`](#classtf__client_1_1TFClient_1ae4c93dbacad72dbb84ed8139442e6864)`(self,message)` 

Generated by [Moxygen](https://sourcey.com/moxygen)