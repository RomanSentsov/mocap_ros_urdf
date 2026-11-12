# Introduction

Visualization tool for unitree g1 axis studio teleop (Modified https://github.com/pnmocap/mocap_ros_urdf.git)

requires ros2 (tested on humble)

# build:

```
cd ~/mocap_ros_urdf
colcon build
source install/setub.bash
```

# run:

```
cd ~/mocap_ros_urdf
source install/setup.bash
ros2 launch unitree_g1_ros2 display.launch.py
```

Broken robot model is normal until first retarget command is received
