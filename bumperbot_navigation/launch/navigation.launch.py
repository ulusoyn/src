import os
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution


def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time")
    map_file = LaunchConfiguration("map_file")
    nav2_config = LaunchConfiguration("nav2_config")

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true"
    )

    map_arg = DeclareLaunchArgument(
        "map_file",
        default_value=os.path.join(
            get_package_share_directory("bumperbot_mapping"),
            "maps",
            "map.yaml"
        )
    )

    nav2_config_arg = DeclareLaunchArgument(
        "nav2_config",
        default_value=os.path.join(
            get_package_share_directory("bumperbot_navigation"),
            "config",
            "navigation_config.yaml"
        )
    )

    navigation = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("nav2_bringup"),
            "launch",
            "navigation_launch.py"
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "map": map_file,
            "params_file": nav2_config
        }.items()
    )


    return LaunchDescription([
        map_arg,
        use_sim_time_arg,
        nav2_config_arg,
        navigation
    ])