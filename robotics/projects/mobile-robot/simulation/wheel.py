"""
I guess we need to reinvent it lol
"""
from dataclasses import dataclass


@dataclass
class Wheel:
    """ Has a size (radius) and a traction) """
    radius: float
    traction: float = 1.0  # 1 implies no slippage

    def angular_velocity(self, rim_velocity: float,) -> float:
        """ What it says on the tin """
        return rim_velocity / self.radius

    def ground_velocity(self, rim_velocity: float,) -> float:
        """ What it says on the tin """
        return self.traction * rim_velocity
