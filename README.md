# ros-mon-ma

## Prerequisites

Setup PC and ROS Noetic Ninjemys according to ROBOTIS eManual: https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/#pc-setup

Setup Gazebo Simulation for ROS Noetic Ninjemys according to ROBOTIS eManual: https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/#gazebo-simulation

## Bringup

### In Console

```roscore```

```roslaunch rosbridge_server rosbridge_websocket.launch```

```rosrun tf2_web_republisher tf2_web_republisher```

```roslaunch turtlebot3_gazebo multi_turtlebot3.launch```

### Backend

```python manage.py runserver --noreload```

### Frontend

```ng serve``` (via runner in package.json)
