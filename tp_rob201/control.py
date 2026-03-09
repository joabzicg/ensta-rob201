""" A set of robotics control functions """

import random
import numpy as np


def reactive_obst_avoid(lidar):
    """
    Simple obstacle avoidance
    lidar : placebot object with lidar data
    """
    # TODO for TP1

    laser_dist = lidar.get_sensor_values()
    ray_angles = lidar.get_ray_angles()

    front_mask = np.abs(ray_angles) < np.deg2rad(25)
    front_dist = laser_dist[front_mask]
    front_dist = front_dist[np.isfinite(front_dist)]

    obstacle_detected = front_dist.size > 0 and np.min(front_dist) < 30

    if not hasattr(reactive_obst_avoid, "turn_steps"):
        reactive_obst_avoid.turn_steps = 0
        reactive_obst_avoid.turn_direction = 0.0

    if obstacle_detected and reactive_obst_avoid.turn_steps == 0:
        reactive_obst_avoid.turn_steps = random.randint(8, 18)
        reactive_obst_avoid.turn_direction = random.choice([-0.8, 0.8])

    if reactive_obst_avoid.turn_steps > 0:
        speed = 0.0
        rotation_speed = reactive_obst_avoid.turn_direction
        reactive_obst_avoid.turn_steps -= 1
    else:
        speed = 0.4
        rotation_speed = 0.0

    command = {"forward": speed,
               "rotation": rotation_speed}

    return command


def potential_field_control(lidar, current_pose, goal_pose):
    """
    Control using potential field for goal reaching and obstacle avoidance
    lidar : placebot object with lidar data
    current_pose : [x, y, theta] nparray, current pose in odom or world frame
    goal_pose : [x, y, theta] nparray, target pose in odom or world frame
    Notes: As lidar and odom are local only data, goal and gradient will be defined either in
    robot (x,y) frame (centered on robot, x forward, y on left) or in odom (centered / aligned
    on initial pose, x forward, y on left)
    """
    # TODO for TP2

    command = {"forward": 0,
               "rotation": 0}

    return command
