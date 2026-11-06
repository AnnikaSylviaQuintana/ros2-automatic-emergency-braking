# ROS2 Automatic Emergency Braking

An Automatic Emergency Braking (AEB) system developed using ROS2 Humble and tested in the F1TENTH racing simulator.

## Project Overview

This project implements a safety node that uses LiDAR sensor readings and vehicle odometry to estimate the instantaneous time to collision (iTTC) with nearby obstacles.

When the calculated iTTC falls below a threshold of 0.8 seconds, the node publishes a zero-speed command to stop the simulated vehicle.

## Technologies Used

- ROS2 Humble
- Python
- Ubuntu 22.04 (WSL2)
- F1TENTH Simulator
- RViz2

## How It Works

The safety node:

1. Subscribes to `/scan` for LiDAR distance measurements.
2. Subscribes to `/ego_racecar/odom` for vehicle velocity.
3. Calculates the rate of approach to obstacles using the vehicle's speed and LiDAR beam angles.
4. Calculates iTTC for valid LiDAR readings.
5. Publishes an emergency stop command to `/drive` when the minimum iTTC is below 0.8 seconds.

## Testing

The node was tested using the F1TENTH simulator with ROS2 Humble.

During testing, the simulated vehicle was commanded to drive forward at 1.0 m/s and stopped before reaching a wall.

## Demonstration

[Watch the Automatic Emergency Braking Demo](https://github.com/AnnikaSylviaQuintana/ros2-automatic-emergency-braking/blob/main/ROS2_Automatic_Emergency_Braking_Demo.mp4.mp4)

## Acknowledgements

Developed as part of the RoboRacer learning modules for the TMU Velocity robotics team. Based on the F1TENTH course materials.
