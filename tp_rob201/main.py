""" A simple SLAM demonstration using the "placebot" robot simulator """

import arcade
from pathlib import Path

from place_bot.simulation.ray_sensors.lidar import LidarParams
from place_bot.simulation.robot.odometer import OdometerParams
from place_bot.simulation.gui_map.keyboard_controller import KeyboardController
from place_bot.simulation.gui_map.simulator import Simulator

from my_robot_slam import MyRobotSlam

from worlds.my_world import MyWorld


def enable_wasd_keyboard_control():
    """Extend the simulator keyboard controller to support WASD in addition to arrows."""

    def on_key_press(self, key: int, modifiers: int) -> None:
        if self._command:
            if key in (arcade.key.UP, arcade.key.W):
                self._command["forward"] = 1.0
            elif key in (arcade.key.DOWN, arcade.key.S):
                self._command["forward"] = -1.0

            if key in (arcade.key.LEFT, arcade.key.A):
                self._command["rotation"] = 1.0
            elif key in (arcade.key.RIGHT, arcade.key.D):
                self._command["rotation"] = -1.0

    def on_key_release(self, key: int, modifiers: int) -> None:
        if self._command:
            if key in (arcade.key.UP, arcade.key.W, arcade.key.DOWN, arcade.key.S):
                self._command["forward"] = 0.0

            if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
                self._command["rotation"] = 0.0

    KeyboardController.on_key_press = on_key_press
    KeyboardController.on_key_release = on_key_release

if __name__ == '__main__':
    enable_wasd_keyboard_control()

    lidar_params = LidarParams()
    lidar_params.noise_enable = False
    # lidar_params.fov = 360
    # lidar_params.resolution = 361
    # lidar_params.max_range = 600
    # lidar_params.std_dev_noise = 2.5

    odometer_params = OdometerParams()
    odometer_params.param1 = 0.0
    odometer_params.param2 = 0.0
    odometer_params.param3 = 0.0
    odometer_params.param4 = 0.0

    # Using shaders allows you to take advantage of the GPU's computing power. Occasionally, on certain machines,
    # notably Windows and macOS, the semantic sensor and lidar may behave in unexpected or aberrant ways.
    # In such cases, you need to disable the shaders.
    use_shaders = True

    my_robot = MyRobotSlam(lidar_params=lidar_params,
                           odometer_params=odometer_params)
    my_world = MyWorld(robot=my_robot, use_shaders=use_shaders)
    simulator = Simulator(the_world=my_world,
                          use_keyboard=True)

    simulator.run()

    output_dir = Path(__file__).resolve().parent.parent / "generated_maps"
    output_dir.mkdir(exist_ok=True)
    output_base = output_dir / "manual_map_latest"
    my_robot.occupancy_grid.save(str(output_base))
