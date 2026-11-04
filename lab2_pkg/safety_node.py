# Imports and setup
import rclpy
import math
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from ackermann_msgs.msg import AckermannDriveStamped


class SafetyNode(Node):
    def __init__(self):
        super().__init__('safety_node')
        # Initialize car speed to 0
        self.speed = 0.0

	# Three ROS2 connections:
        # Subscribe to LiDAR data
        self.scan_subscription = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        # Subscribe to odometry data
        self.odom_subscription = self.create_subscription(Odometry, '/ego_racecar/odom', self.odom_callback, 10)
        # Publish emergency braking commands
        self.drive_publisher = self.create_publisher(AckermannDriveStamped, '/drive', 10)

    def odom_callback(self, msg):
        # Update the current speed
        self.speed = msg.twist.twist.linear.x

    def scan_callback(self, msg):
        # Get LiDAR ranges and angles (distance)
        ranges = msg.ranges
        angle_min = msg.angle_min
        angle_increment = msg.angle_increment
	
        car_range_rates = []
        for i in range(len(ranges)):
                angle = angle_min + i * angle_increment
		# Expected rate of change for the current LiDAR beam
                current_range_rate = -self.speed * math.cos(angle)
                car_range_rates.append(current_range_rate)
	
        ittc_values = []
        for i in range(len(ranges)):
                distance = ranges[i]
                closing_speed = max(-car_range_rates[i], 0.0)
		# Check for invalid or out-of-range LiDAR readings
                if not math.isfinite(distance) or distance < msg.range_min or distance > msg.range_max:
                        current_ittc = math.inf
		# Check if the car is not approaching an obstacle 
                elif closing_speed == 0:
                        current_ittc = math.inf
		# Else distance is valid and the car is getting closer to the obstacle in the beam
                else:
                        current_ittc = distance / closing_speed

                ittc_values.append(current_ittc)
	# Determine whether to brake
	# Braking threshold (seconds) 
        ittc_threshold = 0.8
	# Brake if the minimum iTTC is below the threshold
        if min(ittc_values) < ittc_threshold:
                self.brake()

    def brake(self):
        # Stop the car
        brake_msg = AckermannDriveStamped()
        brake_msg.drive.speed = 0.0
	# Publish a zero-speed command
        self.drive_publisher.publish(brake_msg)


def main(args=None):
    rclpy.init(args=args)
    node = SafetyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
