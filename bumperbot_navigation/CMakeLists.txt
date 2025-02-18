cmake_minimum_required(VERSION 3.8)
project(bumperbot_navigation)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(robot_interfaces REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rosidl_default_runtime REQUIRED)

install(
  PROGRAMS
    bumperbot_navigation/simple_commander.py
  DESTINATION lib/${PROJECT_NAME}
)


install(
  DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
