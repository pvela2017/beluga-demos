#!/usr/bin/python3

# Copyright 2023 Ekumen, Inc.
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
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():
    input_type_conf = LaunchConfiguration('input_type')

    input_type_arg = DeclareLaunchArgument(
        name='input_type',
        default_value='keyboard',
        description='Operator input method',
        choices=['keyboard', 'gamepad'],
    )

    keyboard_teleop_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory('beluga_demo_teleop'), 'launch'
                ),
                '/teleop_input_keyboard_launch.py',
            ]
        ),
        condition=IfCondition(
            PythonExpression(['"', input_type_conf, '" == "keyboard"']),
        ),
    )

    gamepad_xbox_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory('beluga_demo_teleop'), 'launch'
                ),
                '/teleop_input_gamepad_launch.py',
            ]
        ),
        condition=IfCondition(
            PythonExpression(['"', input_type_conf, '" == "gamepad"'])
        ),
    )

    return LaunchDescription(
        [
            input_type_arg,
            keyboard_teleop_include,
            gamepad_xbox_include,
        ]
    )
