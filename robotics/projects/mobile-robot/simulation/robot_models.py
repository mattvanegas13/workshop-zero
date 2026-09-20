from typing import Type
from dataclasses import dataclass
from abc import ABC, abstractmethod

from .pose import Pose
from .wheel import Wheel
from .encoders import Encoder
from .odometry import SensorData, odometry_update
from .kinematics import propagate_ground_truth


@dataclass(frozen=True)
class ConfigurationParam:
    """ Object that contains simulated robot specifications """
    r_l: float = 0.1
    r_r: float = 0.1
    wheel_base: float = 0.5
    ticks_per_revolution: int = 36
    traction_l: float = 1.0
    traction_r: float = 1.0


class MobileRobot(ABC):
    """ Mobile robot interface"""
    @abstractmethod
    def reset(self) -> None:
        """Reset any internal robot or sensor state."""

    @abstractmethod
    def ground_truth_step(self, p: Pose, v_l: float,
                          v_r: float, dt: float) -> Pose:
        """Advance the robot's true pose over one simulation step."""

    @abstractmethod
    def sensor_step(self, v_l: float, v_r: float, dt: float) -> SensorData:
        """Generate sensor measurements for one simulation step."""

    @abstractmethod
    def odometry_step(self, p: Pose, sensor_data: SensorData) -> Pose:
        """Estimate the next pose from the current sensor measurements."""


class DifferentialDriveRobot(MobileRobot):
    """ Simple differential drive robot """

    def __init__(self, config: ConfigurationParam | None = None, encoder_type: Type[Encoder] = Encoder,) -> None:
        self.config = config or ConfigurationParam()

        self.left_wheel = Wheel(self.config.r_l, self.config.traction_l)
        self.right_wheel = Wheel(self.config.r_r, self.config.traction_r)

        self.left_encoder = encoder_type(self.config.ticks_per_revolution)
        self.right_encoder = encoder_type(self.config.ticks_per_revolution)

    def reset(self) -> None:
        self.left_encoder.reset()
        self.right_encoder.reset()

    def ground_truth_step(self, p: Pose, v_l: float, v_r: float, dt: float) -> Pose:
        return propagate_ground_truth(
            p,
            self.left_wheel.ground_velocity(v_l),
            self.right_wheel.ground_velocity(v_r),
            self.config.wheel_base,
            dt,
        )

    def sensor_step(self, v_l: float, v_r: float, dt: float) -> SensorData:
        left = self.left_encoder.read(
            self.left_wheel.angular_velocity(v_l), dt)
        right = self.right_encoder.read(
            self.right_wheel.angular_velocity(v_r), dt)
        return SensorData(left, right)

    def odometry_step(self, p: Pose, sensor_data: SensorData) -> Pose:
        return odometry_update(
            p,
            sensor_data,
            self.left_wheel.radius,
            self.right_wheel.radius,
            self.config.wheel_base,
        )
