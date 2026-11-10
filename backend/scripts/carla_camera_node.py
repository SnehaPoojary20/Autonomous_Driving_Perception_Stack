"""ROS2 node: spawns CARLA car + RGB camera, publishes /camera/image_raw. Start CARLA first (./CarlaUE4.sh)."""
import carla, rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

class CarlaCam(Node):
    def __init__(self):
        super().__init__("carla_camera")
        self.pub = self.create_publisher(Image, "/camera/image_raw", 10)
        world = carla.Client("localhost", 2000).get_world()
        bp = world.get_blueprint_library()
        car = world.spawn_actor(bp.filter("vehicle.tesla.model3")[0], world.get_map().get_spawn_points()[0])
        car.set_autopilot(True)
        cb = bp.find("sensor.camera.rgb"); cb.set_attribute("image_size_x", "1280"); cb.set_attribute("image_size_y", "720")
        world.spawn_actor(cb, carla.Transform(carla.Location(x=1.5, z=1.6)), attach_to=car).listen(self.on_img)

    def on_img(self, im):
        m = Image(); m.height, m.width, m.encoding = im.height, im.width, "bgra8"
        m.step = im.width * 4; m.data = bytes(im.raw_data)
        self.pub.publish(m)

rclpy.init(); rclpy.spin(CarlaCam())
