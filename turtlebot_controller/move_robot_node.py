#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from  geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

def get_yaw_from_quaternion(q):
    siny_cosp = 2 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


class Move_Robot_Node(Node):
    def __init__(self):
        super().__init__("Move_Robot_Node")
        self.get_logger().info("Hareket başlatildi!")
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscriptions_ = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10)
        
        self.target_x = 10.0
        self.target_y = 7.5

   
    def odom_callback(self, msg):
        current_x = msg.pose.pose.position.x
        current_y = msg.pose.pose.position.y
        
        diff_x = self.target_x - current_x
        diff_y = self.target_y - current_y
        
        distance = math.sqrt(diff_x**2 + diff_y**2)
        target_angle = math.atan2(diff_y, diff_x)
        current_yaw = get_yaw_from_quaternion(msg.pose.pose.orientation)
        angle_error = target_angle - current_yaw
        
        cmd = Twist()
        
        if abs(angle_error) > 0.2:
            cmd.angular.z = angle_error
            cmd.linear.x = 0.0
        else:
            if distance >= 1.0:
                cmd.linear.x = 0.5  
            elif distance > 0.1:
                cmd.linear.x = 0.15 
            else:
                cmd.linear.x = 0.0  
                self.get_logger().info("Hedefe ulaşildi!")

            cmd.angular.z = 0.0
            
        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)    
    node = Move_Robot_Node()          
    rclpy.spin(node)         
    rclpy.shutdown()          
if __name__ == '__main__':
    main()
