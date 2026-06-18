#!/usr/bin/env python3

import serial

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool


class SerialReaderNode(Node):
    def __init__(self):
        super().__init__('serial_reader_node')

        # Declare parameters
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('threshold', 1.0)

        # Get parameters
        self.port = self.get_parameter('port').get_parameter_value().string_value
        self.baudrate = self.get_parameter('baudrate').get_parameter_value().integer_value
        self.threshold = self.get_parameter('threshold').get_parameter_value().double_value

        # Create publishers
        self.raw_data_pub = self.create_publisher(String, 'raw_serial_data', 10)
        self.collision_pub = self.create_publisher(Bool, 'collision_detected', 10)

        # Open serial port
        try:
            self.serial_port = serial.Serial(self.port, self.baudrate, timeout=0.1)
            self.get_logger().info(f"Opened serial port {self.port} at {self.baudrate} baud")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to open serial port {self.port} at {self.baudrate} baud: {e}")
            raise

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
