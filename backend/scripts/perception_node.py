"""ROS2 node: /camera/image_raw -> perception -> /perception/image + /perception/detections (JSON string)."""
import sys, json, rclpy, numpy as np, cv2
sys.path.insert(0, ".")
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from app.pipeline.perception import Perception

class PerceptionNode(Node):
    def __init__(self):
        super().__init__("perception")
        self.p = Perception()
        self.create_subscription(Image, "/camera/image_raw", self.cb, 10)
        self.img_pub = self.create_publisher(Image, "/perception/image", 10)
        self.det_pub = self.create_publisher(String, "/perception/detections", 10)

    def cb(self, m):
        f = cv2.cvtColor(np.frombuffer(m.data, np.uint8).reshape(m.height, m.width, 4), cv2.COLOR_BGRA2BGR)
        out, meta = self.p.run(f)
        o = Image(); o.height, o.width, o.encoding, o.step = out.shape[0], out.shape[1], "bgr8", out.shape[1] * 3
        o.data = out.tobytes(); self.img_pub.publish(o)
        self.det_pub.publish(String(data=json.dumps(meta)))
        near = [x for x in meta["objects"] if x["distance_m"] < 8]
        if near: self.get_logger().warn(f"BRAKE: {near[0]['cls']} at {near[0]['distance_m']} m")

rclpy.init(); rclpy.spin(PerceptionNode())
