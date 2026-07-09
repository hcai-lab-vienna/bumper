#!/usr/bin/env python3

import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist


class CollisionResponseNode(Node):

# -----------------------------------------------------------------------------
# CHANGES THIS for different segment motion routines
    def collision_commands(self, segment_number:int=0) -> list[tuple]:
        """
        Returns motion routine for a segment when collision happens.
        If no segment_number is provided, returns the default motion routine.
        """
        # set self.speed with ros variable speed, default 0.5

        if segment_number == 1:
            a2 = self.speed * random.choice([-1, 1])
            d2 = random.uniform(2, 6)
            return [
                # linear, angular, duration
                (-self.speed, 0.0, 1.5),
                (0.0, a2, d2),
                self.collision_commands()[0]
            ].copy()

        # default motion routine (drive forwards)
        return [(self.speed, 0.0, 0.0)].copy()
# -----------------------------------------------------------------------------

    def __init__(self):
        super().__init__('collision_response_node')
        self.create_subscription(Int8, '/collision_detected', self.collision_callback, 10)
        self.cmd_vel = self.create_publisher(Twist, '/cmd_vel', 10)
        # static speed and motion values
        self.declare_parameter('speed', 0.5)
        self.speed = self.get_parameter('speed').get_parameter_value().double_value
        # current motion, will be constantly changed during execution
        self.linear, self.angular, self.duration = self.collision_commands()[0]
        # command_stack will be executed by the robot from top to bottom,
        # each command is a tuple of (linear speed, angular speed, duration in seconds).
        self.command_stack = []
        # timer for each command executed by command_stack, last filed of each command_stack tuple will be the duration.
        self.command_timer = self.create_timer(0, lambda: None)
        self.command_timer.cancel()

    def schedule_command(self):
        "Schedules commands from command_stack and waits duration for next command (recursive)."
        self.command_timer.cancel()
        if self.command_stack:
            self.stop()
            self.linear, self.angular, self.duration = map(float, self.command_stack.pop(0))
            if self.duration:
                self.command_timer = self.create_timer(self.duration, self.schedule_command)
            # else:
            #   run the last command for ever

    def collision_callback(self, msg: Int8):
        """
        The topic '/collision_detected' constantly publishes 0 (no collision) or segment number (collision).
        Therefore this callback is continuously executed with the frequency specified in serial_reader_node.py
        """
        # msg.data is zero if no collision was detected,
        # otherwise it is a positive number indicating the segment number
        # of the segment where a collision was detected.
        if msg.data and not self.command_stack: # if there is a collision (msg.data != 0) and no commands currently executed
            self.command_stack = self.collision_commands(msg.data) # populate the command stack
        if self.command_timer.is_canceled(): # if the robot currently executes a command for self.duration, don't schedule a new one
            self.schedule_command() # schedule the next command and start a timer, this is RECURSIVE
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
