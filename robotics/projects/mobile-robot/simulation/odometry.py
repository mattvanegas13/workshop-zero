from dataclasses import dataclass
from math import cos, sin, pi

from .pose import Pose
from .encoders import EncoderReading


@dataclass
class SensorData:
    """ Snapshot of what the wheels are doing """
    left_wheel_sensor_reading: EncoderReading
    right_wheel_sensor_reading: EncoderReading


def angular_displacement(reading: EncoderReading) -> float:
    """ how many radians the wheel moves based on the emmitted ticks we see from the encoder """
    return (2 * pi * reading.delta_ticks) / reading.ticks_per_revolution


def linear_displacement(reading: EncoderReading, wheel_radius: float) -> float:
    """ linear distance the robot traveled based on its angular displacement """
    return wheel_radius * angular_displacement(reading)


def odometry_update(p: Pose, sensor_data: SensorData, left_wheel_radius: float, right_wheel_radius: float, wheel_base: float) -> Pose:
    """ Reconstruct motion based on its measurements """
    delta_s_l = linear_displacement(
        sensor_data.left_wheel_sensor_reading, left_wheel_radius)
    delta_s_r = linear_displacement(
        sensor_data.right_wheel_sensor_reading, right_wheel_radius)
    delta_theta = (delta_s_r - delta_s_l) / wheel_base
    delta_s = (delta_s_l + delta_s_r) / 2
    midpoint_theta = (p.theta + delta_theta / 2)
    x_new = (p.x + delta_s * cos(midpoint_theta))
    y_new = (p.y + delta_s * sin(midpoint_theta))
    theta_new = (p.theta + delta_theta)
    return Pose(x=x_new, y=y_new, theta=theta_new)
