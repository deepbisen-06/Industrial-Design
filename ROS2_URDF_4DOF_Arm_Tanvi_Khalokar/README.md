# ROS2 URDF 4-DOF Arm — Tanvi Khalokar

Open report.pdf. The arm_description folder is an ament_cmake ROS2 description package with URDF, launch file and RViz configuration.

## ROS2 Humble / Ubuntu 22.04
Install ROS2 Humble following https://docs.ros.org/en/humble/Installation.html, then:

    sudo apt update
    sudo apt install ros-humble-robot-state-publisher ros-humble-joint-state-publisher-gui ros-humble-rviz2 ros-humble-tf2-tools ros-humble-tf2-ros python3-colcon-common-extensions liburdfdom-tools
    source /opt/ros/humble/setup.bash
    mkdir -p ~/ros2_ws/src
    cp -r arm_description ~/ros2_ws/src/
    cd ~/ros2_ws
    colcon build --symlink-install --packages-select arm_description
    source install/setup.bash
    check_urdf src/arm_description/urdf/industrial_arm.urdf
    ros2 launch arm_description display.launch.py

Use a graphical desktop. If your machine already uses a different workspace, use that workspace rather than overwriting files. Humble is the chosen target; the package was not runtime-tested on Humble or Iron. The assignment also allows Iron, but do not assume cross-distro results.

In RViz set Fixed Frame=world. The supplied config enables RobotModel, TF and Grid. RobotModel uses the transient-local /robot_description topic. If a GUI version fails to restore settings, add RobotModel manually and select that topic with compatible QoS. Move the four joint-state sliders individually; watch rotation about local Z for joint1 and local Y for joints2-4.

In another terminal, source BOTH ROS and workspace setup:

    ros2 topic list
    ros2 topic echo /joint_states --once
    ros2 run tf2_tools view_frames
    ros2 run tf2_ros tf2_echo world tool_link

The view_frames command writes its frames PDF in the current directory (filename can vary by ROS2 version). Record the actual output and do not confuse the static graph supplied here with live TF evidence. Home tool-frame position should be (0, 0, 0.87) m; distal tool face is at Z=0.93 m.

## Existing static verification

    python -m pip install numpy urdf-parser-py pyyaml
    python verification/validate_model.py

These checks were executed. See evidence/validation_results.txt and evidence/fk_results.json. They do not prove ROS2 launch or RViz success. The validation FK routine is intentionally limited to this model's zero-RPY joint origins.

## Complete the required evidence
Add genuine screenshots of RViz home and bent poses, GUI sliders, and generated live TF frames PDF. Record /joint_states and tf2_echo output. Update the report with actual observations. A real ROS2 runtime was unavailable in the preparation environment, so those screenshots are not supplied or fabricated.

Upload report, package and actual screenshots to Google Drive in ROS2_URDF_4DOF_Arm_Tanvi_Khalokar and share the link as required by the assignment.

The effort/velocity limits and masses are educational assumptions. The model is kinematic, not a validated industrial machine; no Gazebo controller, actuator sizing, self-collision planning, or dynamic simulation is included.
