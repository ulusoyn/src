cmake_minimum_required(VERSION 3.8)
project(robot_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generate the interface
rosidl_generate_interfaces(
  ${PROJECT_NAME}
  "msg/RobotPose.msg"
  "msg/RobotDestination.msg"
)

# Ensure ament packaging is defined after generating interfaces
ament_package()
