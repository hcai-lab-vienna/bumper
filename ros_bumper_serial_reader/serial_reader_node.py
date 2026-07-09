#!/usr/bin/env python3

import serial

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int8


class SerialReaderNode(Node):

    def __init__(self):
        super().__init__('serial_reader_node')
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.port = self.get_parameter('port').get_parameter_value().string_value
        self.declare_parameter('segment_number', 1)
        self.segment_number = self.get_parameter('segment_number').get_parameter_value().integer_value
        if self.segment_number < 1:
            e = ValueError(f"Segment number must be greater than 0, got {self.segment_number}")
            self.get_logger().error(f"Failed to set segment number: {e}")
            raise e
        self.declare_parameter('threshold', 100.0)
        self.threshold = self.get_parameter('threshold').get_parameter_value().double_value
        self.collision_pub = self.create_publisher(Int8, 'collision_detected', 10)
        try:
            self.serial_port = serial.Serial(self.port, baudrate=115200, timeout=0.1)
            self.get_logger().info(f"Opened serial port {self.port}")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to open serial port: {e}")
            raise e
        self.timer = self.create_timer(0.01, self.read_serial)

    def read_serial(self):
        try:
            while self.serial_port.in_waiting > 0:
                line = self.serial_port.readline().decode('utf-8').strip()
                if line:
                    self.process_and_publish_line(line)
        except serial.SerialException as e:
            self.get_logger().error(f"Serial read error: {e}")

    def process_and_publish_line(self, line):
        try:
            s1, s2 = map(float, line.split(','))
            condition = abs(s1) > self.threshold or abs(s2) > self.threshold
            msg = Int8()
            msg.data = self.segment_number if condition else 0
            self.collision_pub.publish(msg)
            if condition:
                self.get_logger().info(f"Collision detected in segment {self.segment_number:2d}: {s1:7.1f} {s2:7.1f}  threshold={self.threshold}")
        except (ValueError, IndexError) as e:
            self.get_logger().warn(f"Failed to parse line: {line}. Error: {e}")

    def destroy_node(self):
        if hasattr(self, 'serial_port') and self.serial_port.is_open:
            self.serial_port.close()
            self.get_logger().info("Closed serial port")
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SerialReaderNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
