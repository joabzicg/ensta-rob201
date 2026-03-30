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
        speed = 0.9
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
    """

    # Parameters
    K_goal = 0.02
    K_obs = 500.0
    d_goal_stop = 30.0
    d_safe = 120.0
    eps = 1e-3

    # Attractive component (world frame)
    q = np.array(current_pose[:2], dtype=float)
    q_goal = np.array(goal_pose[:2], dtype=float)
    diff_goal = q_goal - q
    dist_goal = np.linalg.norm(diff_goal)

    if dist_goal < eps:
        return {"forward": 0.0, "rotation": 0.0}

    if dist_goal < d_goal_stop:
        # quadratic approach near goal
        u_att = K_goal * diff_goal
    else:
        u_att = K_goal * diff_goal / dist_goal

    # Repulsive component (world frame) using closest obstacle from lidar
    ranges = lidar.get_sensor_values()
    angles = lidar.get_ray_angles()
    valid = np.isfinite(ranges)
    ranges = ranges[valid]
    angles = angles[valid]

    u_rep = np.zeros(2, dtype=float)
    if ranges.size > 0:
        idx = np.argmin(ranges)
        d_obs = ranges[idx]
        if d_obs < d_safe and d_obs > eps:
            # obstacle in robot frame
            obs_robot = np.array([d_obs * np.cos(angles[idx]), d_obs * np.sin(angles[idx])])
            # repulsion in robot frame (away from obstacle)
            rep_robot = (1.0 / d_obs - 1.0 / d_safe) * (1.0 / (d_obs**2)) * (-obs_robot)
            # transform to world frame
            theta = current_pose[2]
            c, s = np.cos(theta), np.sin(theta)
            u_rep = np.array([[c, -s], [s, c]]).dot(rep_robot)

    # Resultant vector in world frame
    u_world = u_att + u_rep

    # Convert desired action to robot frame
    theta = current_pose[2]
    c, s = np.cos(theta), np.sin(theta)
    u_robot = np.array([[c, s], [-s, c]]).dot(u_world)
    dx, dy = u_robot

    desired_angle = np.arctan2(dy, dx)
    forward_speed = np.clip(np.linalg.norm(u_robot), 0.0, 1.0)

    # Slow down near goal
    if dist_goal < d_goal_stop:
        forward_speed *= (dist_goal / d_goal_stop)

    rotation_speed = np.clip(2.5 * desired_angle, -1.0, 1.0)

    # Avoid moving backwards if goal is behind: rotate in place
    if dx < 0:
        forward_speed = 0.0

    # final command
    command = {"forward": float(forward_speed), "rotation": float(rotation_speed)}

    # Stop when very close to goal
    if dist_goal < 2.0:
        command = {"forward": 0.0, "rotation": 0.0}

    return command
