""" A simple robotics navigation code including SLAM, exploration, planning"""

import cv2
import numpy as np
from occupancy_grid import OccupancyGrid


class TinySlam:
    """Simple occupancy grid SLAM"""

    def __init__(self, occupancy_grid: OccupancyGrid):
        self.grid = occupancy_grid

        # Origin of the odom frame in the map frame
        self.odom_pose_ref = np.array([0, 0, 0])
        self._last_map_pose = None

    def _score(self, lidar, pose):
        """
        Computes the sum of log probabilities of laser end points in the map
        lidar : placebot object with lidar data
        pose : [x, y, theta] nparray, position of the robot to evaluate, in world coordinates
        """
        # TODO for TP4

        score = 0

        return score

    def get_corrected_pose(self, odom_pose, odom_pose_ref=None):
        """
        Compute corrected pose in map frame from raw odom pose + odom frame pose,
        either given as second param or using the ref from the object
        odom : raw odometry position
        odom_pose_ref : optional, origin of the odom frame if given,
                        use self.odom_pose_ref if not given
        """
        # TODO for TP4
        corrected_pose = odom_pose

        return corrected_pose

    def localise(self, lidar, raw_odom_pose):
        """
        Compute the robot position wrt the map, and updates the odometry reference
        lidar : placebot object with lidar data
        odom : [x, y, theta] nparray, raw odometry position
        """
        # TODO for TP4

        best_score = 0

        return best_score

    def update_map(self, lidar, pose):
        """
        Bayesian map update with new observation
        lidar : placebot object with lidar data
        pose : [x, y, theta] nparray, corrected pose in world coordinates
        """
        free_update = -0.08
        occupied_update = 0.4
        clip_min = -4.0
        clip_max = 4.0
        hit_margin = 4.0
        free_margin = 4.0
        min_translation_update = 2.0
        min_rotation_update = np.deg2rad(1.5)

        pose = np.array(pose, dtype=float)

        if self._last_map_pose is not None:
            delta_translation = np.linalg.norm(pose[:2] - self._last_map_pose[:2])
            delta_rotation = abs(np.arctan2(np.sin(pose[2] - self._last_map_pose[2]),
                                            np.cos(pose[2] - self._last_map_pose[2])))
            if delta_translation < min_translation_update and delta_rotation < min_rotation_update:
                return

        self._last_map_pose = pose.copy()

        ranges = lidar.get_sensor_values()
        ray_angles = lidar.get_ray_angles()
        max_range = float(lidar.max_range)

        valid = np.logical_and(np.isfinite(ranges), ranges > 0)
        ranges = ranges[valid]
        ray_angles = ray_angles[valid]

        if ranges.size == 0:
            return

        # Reduce the number of rays used at each step to keep the control loop responsive.
        ranges = ranges[::2]
        ray_angles = ray_angles[::2]

        robot_x = float(pose[0])
        robot_y = float(pose[1])
        robot_theta = float(pose[2])

        cos_theta = np.cos(robot_theta)
        sin_theta = np.sin(robot_theta)

        hit_points_x = []
        hit_points_y = []
        hit_cells = set()

        for distance, angle in zip(ranges, ray_angles):
            has_hit = distance < (max_range - hit_margin)
            if not has_hit:
                continue

            usable_distance = distance

            if usable_distance <= free_margin:
                continue

            free_distance = usable_distance - free_margin
            free_x_robot = free_distance * np.cos(angle)
            free_y_robot = free_distance * np.sin(angle)

            free_x_world = robot_x + cos_theta * free_x_robot - sin_theta * free_y_robot
            free_y_world = robot_y + sin_theta * free_x_robot + cos_theta * free_y_robot
            self.grid.add_value_along_line(robot_x, robot_y, free_x_world, free_y_world, free_update)

            if has_hit:
                hit_x_robot = distance * np.cos(angle)
                hit_y_robot = distance * np.sin(angle)
                hit_x_world = robot_x + cos_theta * hit_x_robot - sin_theta * hit_y_robot
                hit_y_world = robot_y + sin_theta * hit_x_robot + cos_theta * hit_y_robot

                hit_cell = self.grid.conv_world_to_map(hit_x_world, hit_y_world)
                if hit_cell not in hit_cells:
                    hit_cells.add(hit_cell)
                    hit_points_x.append(hit_x_world)
                    hit_points_y.append(hit_y_world)

        if hit_points_x:
            self.grid.add_map_points(np.array(hit_points_x), np.array(hit_points_y), occupied_update)

        np.clip(self.grid.occupancy_map, clip_min, clip_max, out=self.grid.occupancy_map)

    def compute(self):
        """ Useles function, just fosr the exercise on using the profiler """
        # Remove after TP1

        ranges = np.random.rand(3600)
        ray_angles = np.arange(-np.pi, np.pi, np.pi / 1800)

        # Poor implementation of polar to cartesian conversion
        points = []
        for i in range(3600):
            pt_x = ranges[i] * np.cos(ray_angles[i])
            pt_y = ranges[i] * np.sin(ray_angles[i])
            points.append([pt_x, pt_y])
