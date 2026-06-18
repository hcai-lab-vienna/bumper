#!/usr/bin/env python3

import serial

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool


class SerialReaderNode(Node):

    def __init__(self):
        super().__init__('serial_reader_node')
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('threshold', 100.0)
        self.port = self.get_parameter('port').get_parameter_value().string_value
        self.baudrate = self.get_parameter('baudrate').get_parameter_value().integer_value
        self.threshold = self.get_parameter('threshold').get_parameter_value().double_value
        self.raw_data_pub = self.create_publisher(String, 'raw_serial_data', 10)
        self.collision_pub = self.create_publisher(Bool, 'collision_detected', 10)
        try:
            self.serial_port = serial.Serial(self.port, self.baudrate, timeout=0.1)
            self.get_logger().info(f"Opened serial port {self.port} at {self.baudrate} baud")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to open serial port: {e}")
            raise
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
        raw_msg = String()
        raw_msg.data = line
        self.raw_data_pub.publish(raw_msg)
        try:
            s1, s2 = map(float, line.split(','))
            collision_msg = Bool()
            collision_msg.data = abs(s1) > self.threshold or abs(s2) > self.threshold
            self.collision_pub.publish(collision_msg)
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
