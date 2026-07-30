#!/usr/bin/env python3

from collections import deque

import rclpy
from matplotlib import pyplot as plt
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class LivePlotter(Node):

    def __init__(self):
        super().__init__('live_plotter')
        self.subscription = self.create_subscription(
            Float64MultiArray,
            '/raw_bumper_data',
            self.listener_callback,
            10
        )

        self.max_len = 100
        self.min_y_ax = 1000
        self.y_ax_val = self.min_y_ax
        self.data_1 = deque(maxlen=self.max_len)
        self.data_2 = deque(maxlen=self.max_len)

        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.line_1, = self.ax.plot([], [], 'b-')
        self.line_2, = self.ax.plot([], [], 'g-')
        self.ax.set_xlim(0, self.max_len)
        self.ax.set_xticks([i for i in range(0, self.max_len+1, 10)])
        self.ax.set_xlabel('data point que')
        self.ax.set_ylabel('serial reading')

    def listener_callback(self, msg):
        self.data_1.append(msg.data[0])
        self.data_2.append(msg.data[1])
        dt = range(len(self.data_1))
        self.line_1.set_data(dt, self.data_1)
        self.line_2.set_data(dt, self.data_2)
        self.y_ax_val = max(
            max(self.data_1),
            max(self.data_2),
            self.y_ax_val*0.9,
            self.min_y_ax
        )
        self.ax.set_ylim(0, self.y_ax_val)
        self.fig.canvas.flush_events()

def main(args=None):
    rclpy.init(args=args)
    live_plotter = LivePlotter()
    rclpy.spin(live_plotter)
    live_plotter.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
