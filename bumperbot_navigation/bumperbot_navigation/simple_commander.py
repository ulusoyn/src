#!/usr/bin/env python3
import rclpy
from robot_interfaces.msg import RobotDestination, RobotPose
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
from rclpy.node import Node

class SimpleCommanderNode(Node):
    def __init__(self):
        super().__init__('simple_commander_node')
        self.pose = PoseStamped()
        self.nav = BasicNavigator()
        self.initial_pose_received = False
        self.publisher_ = self.create_publisher(PoseStamped, 'robot_destination',10)
        self.pose_initializer = self.create_subscription(RobotPose, 'robot_initial_pose', self.pose_callback, 10)
        self.pose_initializer


    def pose_callback(self, msg):
        if not self.initial_pose_received:
            self.pose.header.frame_id = "map"
            self.pose.header.stamp = self.get_clock().now().to_msg()
            self.pose.pose.position.x = msg.x
            self.pose.pose.position.y = msg.y
            self.pose.pose.orientation.z = 0.0

            
            self.nav.setInitialPose(self.pose)
            self.publisher_.publish(self.pose)

            self.destroy_subscription(self.pose_initializer)
            
        
def main(args=None):
    rclpy.init(args=args)
    node = SimpleCommanderNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
