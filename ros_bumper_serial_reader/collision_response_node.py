#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist


class CollisionResponseNode(Node):

    def __init__(self):
        super().__init__('collision_response_node')
        self.declare_parameter('backward_velocity', -1.0)
        self.declare_parameter('cmd_vel_topic', '/cmd_vel')
        self.declare_parameter('cooldown_period', 2.0)
        self.backward_velocity = self.get_parameter('backward_velocity').get_parameter_value().double_value
        self.cmd_vel_topic = self.get_parameter('cmd_vel_topic').get_parameter_value().string_value
        self.cooldown_period = self.get_parameter('cooldown_period').get_parameter_value().double_value
        self.collision_sub = self.create_subscription(
            Bool,
            '/collision_detected',
            self.collision_callback,
            10)
        self.cmd_vel_pub = self.create_publisher(Twist, self.cmd_vel_topic, 10)
        self.last_collision_time = self.get_clock().now()

    def collision_callback(self, msg):
        current_time = self.get_clock().now()
        collision_detected = msg.data
        if collision_detected:
            time_since_last = (current_time - self.last_collision_time).nanoseconds / 1e9
            if time_since_last > self.cooldown_period:
                self.last_collision_time = current_time
                self.publish_backward()

    def publish_backward(self):
        twist = Twist()
        twist.linear.x = self.backward_velocity
        self.cmd_vel_pub.publish(twist)
        self.get_logger().info("Collision detected! Moving backwards.")

    def destroy_node(self):
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CollisionResponseNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
