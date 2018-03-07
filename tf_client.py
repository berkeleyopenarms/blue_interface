class TFClient(): 
    def __init__(self,ip,port, options):
        self.RBC = ROSBridgeClient(ip, port)
        # self.tf_action_client = self.RBC.action_client('/tf2_web_republisher', 'tf2_web_republisher/TFSubscriptionAction')

        self.tf_service_client = self.RBC.service("/republish_tfs", "tf2_web_republisher/RepublishTFs")
        _WORLD_FRAME = ""
        _END_EFFECTOR_FRAME = ""

    def updateGoal():
        goal_msg = {
            "source_frames": _WORLD_FRAME,
            "target_frame": _END_EFFECTOR_FRAME,
            "angular_thres": 2.0,
            "trans_thres": 0.01,
            "rate": 10.0,
            "timeout": 2.0
        }

        self.tf_service_client.request(goal_msg, updateGoal_callback)

    def updateGoal_callback(self, topic_name):
        self._tf_subscriber = self.RBC(topic_name, "geometry_msgs/TransformStamped[]", process_tf_callback)

    def process_tf_callback(self, message):
        print(message)

