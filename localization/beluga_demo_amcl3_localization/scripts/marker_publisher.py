#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import ColorRGBA
from geometry_msgs.msg import Point

class PoseVisualizer(Node):
    def __init__(self):
        super().__init__('pose_marker_node')
        self.pose_subscriber = self.create_subscription(
            PoseStamped,
            '/gt_poses',
            self.pose_callback,
            10
        )

        self.marker_publisher = self.create_publisher(MarkerArray, '/gt_pose_markers', 10)
        self.points = []

    def pose_callback(self, msg: PoseStamped):
        position = msg.pose.position
        # Create a point for visualization
        point = Point()
        point.x = position.x
        point.y = position.y
        point.z = position.z
        self.points.append(point)

        # Create MarkerArray to hold the Marker
        marker_array = MarkerArray()

        # Create the LineStrip marker
        line_strip_marker = Marker()
        line_strip_marker.header.frame_id = 'map' 
        line_strip_marker.header.stamp = self.get_clock().now().to_msg()
        line_strip_marker.id = 0
        line_strip_marker.type = Marker.LINE_STRIP
        line_strip_marker.action = Marker.ADD
        line_strip_marker.scale.x = 0.1  
        line_strip_marker.color = ColorRGBA(r=1.0, g=0.0, b=0.0, a=1.0)

        # Add points to the LineStrip marker
        line_strip_marker.points = self.points
        
        # Add the marker to the MarkerArray
        marker_array.markers.append(line_strip_marker)
        
        # Publish the MarkerArray
        self.marker_publisher.publish(marker_array)

def main(args=None):
    rclpy.init(args=args)
    pose_visualizer = PoseVisualizer()
    rclpy.spin(pose_visualizer)
    pose_visualizer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()