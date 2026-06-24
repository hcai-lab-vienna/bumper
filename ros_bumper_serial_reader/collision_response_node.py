#!/usr/bin/env python3

import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist


class CollisionResponseNode(Node):

    def __init__(self):
        super().__init__('collision_response_node')
        self.collision_sub = self.create_subscription(Bool, '/collision_detected', self.collision_callback, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        # command_stack will be executed by the robot from top to bottom,
        # each command is a tuple of (linear speed, angular speed, duration in seconds).
        self.command_stack = []
        # timer for each command executed by command_stack, last filed of each command_stack tuple will be the duration.
        self.command_timer = self.create_timer(0, lambda: None)
        self.command_timer.cancel()

    @property
    def collision_commands(self) -> list[tuple]:
        "motion routine when collision happens"
        a2 = 0.5 * random.choice([-1, 1])
        d2 = random.uniform(2, 6)
        return [
            # linear, angular, duration
            (-0.5, 0.0, 1.5),
            (0.0, a2, d2),
            (0.5, 0.0, 0.1),
        ].copy()

    def command_callback(self):
        "Schedules commands from command_stack and waits duration for next command (recursive)."
        self.command_timer.cancel()
        if self.command_stack:
            linear, angular, duration = map(float, self.command_stack.pop(0))
            self.move(linear, angular)
            if duration:
                self.command_timer = self.create_timer(duration, self.command_callback)
                self.get_logger().info(f"WAIT sec:{duration:.2f}")

    def collision_callback(self, msg: Bool):
        if msg.data and not self.command_stack:
            self.stop()
            self.command_stack = self.collision_commands
        if self.command_timer.is_canceled():
            self.command_callback()

    def move(self, linear: float, angular: float):
        msg = Twist()
        msg.linear.x = float(linear)
        msg.angular.z = float(angular)
        self.cmd_vel_pub.publish(msg)
        self.get_logger().info(f"MOVE lin:{linear:.1f} ang:{angular:.1f}")

    def stop(self):
        msg = Twist()
        self.cmd_vel_pub.publish(msg)
        self.get_logger().info("Stopped moving.")

    def destroy_node(self):
        self.stop()
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
