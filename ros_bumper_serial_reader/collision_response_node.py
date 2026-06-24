#!/usr/bin/env python3

import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist


class CollisionResponseNode(Node):

    def __init__(self):
        super().__init__('collision_response_node')
        self.create_subscription(Bool, '/collision_detected', self.collision_callback, 10)
        self.cmd_vel = self.create_publisher(Twist, '/cmd_vel', 10)
        # current motion
        self.linear, self.angular, self.duration = (0.5, 0.0, 0.0)
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
            (0.5, 0.0, 0.0),
        ].copy()

    def schedule_command(self):
        "Schedules commands from command_stack and waits duration for next command (recursive)."
        self.command_timer.cancel()
        if self.command_stack:
            self.stop()
            self.linear, self.angular, self.duration = map(float, self.command_stack.pop(0))
            if self.duration:
                self.command_timer = self.create_timer(self.duration, self.schedule_command)

    def collision_callback(self, msg: Bool):
        """
        The topic '/collision_detected' constantly publishes False / True (no collision / collision).
        Therefore this callback is continuously executed with the frequency specified in serial_reader_node.py
        """
        if msg.data and not self.command_stack:
            self.command_stack = self.collision_commands
        if self.command_timer.is_canceled():
            self.schedule_command()
        # Always move for real robots, simulations don't need it.
        self.move()

    def move(self):
        "Sets linear and angular for the robot (self)."
        msg = Twist()
        msg.linear.x = self.linear
        msg.angular.z = self.angular
        self.cmd_vel.publish(msg)
        self.get_logger().info(f"MOVE {self.linear:.1f} {self.angular:.1f}")

    def stop(self):
        "STOP!"
        msg = Twist()
        self.cmd_vel.publish(msg)
        self.get_logger().info("STOP")

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
