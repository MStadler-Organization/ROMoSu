# ROMoSu - Flexible Runtime Monitoring Support for ROS-based Applications

ROS-based robotic applications are becoming increasingly common in various different application domains, performing diverse tasks. Examples include autonomous vehicles, small unmanned systems, as well as industrial applications of Cyber-Physical Production Systems. What all these systems have in common is their tight integration between hardware and software components, and close interactions with humans, e.g., on a shop floor, or autonomously driving robots as part of a warehouse system. 
This, in turn, requires monitoring the behavior of the system at runtime and ensuring that it behaves according to its specified requirements. However, establishing and maintaining runtime monitoring support is a non-trivial task, requiring significant up-front investment and extensive domain knowledge. To alleviate this problem, we present ROMoSu (**RO**S **Mo**nitoring **Su**pport), a flexible runtime monitoring framework for ROS-based systems that allows defining multiple scenarios, or application-specific configurations, taking into account different monitoring needs,  and provides tool support for creating, maintaining, and managing configurations at runtime. 
As part of our evaluation, we have conducted experiments with three different use cases, of both physical and simulated applications. Results confirm that ROMoSu can be successfully used to create monitoring configurations with little effort, create efficient monitors and perform constraint checks based on the collected runtime data. 

## Prerequisites for build from source-code

Setup PC and ROS Noetic Ninjemys according to ROBOTIS eManual: https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/#pc-setup

Setup Gazebo Simulation for ROS Noetic Ninjemys according to ROBOTIS eManual: https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/#gazebo-simulation

NodeJS Version with AngularCLI support is required (e.g., 16.10)

Run npm install in Frontend.

Install prerequisites for backend specified in [Backend Readme](https://github.com/MStadler-Organization/ros-mon-ma/tree/main/backend)

## Bringup

### Console

```roscore```

```roslaunch rosbridge_server rosbridge_websocket.launch```

```rosrun tf2_web_republisher tf2_web_republisher```

```roslaunch turtlebot3_gazebo multi_turtlebot3.launch```

### Backend

```python manage.py runserver --noreload```

### Frontend

```ng serve``` (via runner in package.json)
