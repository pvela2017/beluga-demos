# Copyright 2024 Ekumen, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument


import os


def generate_launch_description():
    rviz_config_file = PathJoinSubstitution(
                [
                    FindPackageShare("beluga_demo_amcl3_localization"),
                    "config",
                    "rviz.rviz",
                ]
            ),
    return LaunchDescription(
        [
            Node(
                package="beluga_demo_amcl3_localization",
                executable="beluga_amcl3_demo_node",
                name="beluga_amcl3_demo",
                output="screen",
            ),

            Node(
                package='tf2_ros',
                executable='static_transform_publisher',
                name='velodyne_in_xsense',
                arguments = ['0.0584867781527745', '0.00840419966766332', '0.168915521980526', '0.0078031', '0.0015042', '-0.0252884', 'base_link', 'velodyne']
            ),

            Node(
                package='beluga_demo_amcl3_localization',
                executable='tf_publisher.py',
                name='odom_to_base_link',
                parameters = [{'use_sim_time': True}],
            ),

            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                parameters=[{'use_sim_time': True}],
                arguments=["-d", rviz_config_file],
            ),
        ]
    )
