"""
Contains the methodology to update our position with respect 
to a a given frame of reference 
"""

from dataclasses import dataclass
from math import cos, sin, isclose


@dataclass
class Pose:
    """ Where in the position space we are """
    x: float
    y: float
    theta: float


def update_pose_euler(p: Pose, dt: float, v: float, omega: float) -> Pose:
    """ Use euler forward integration to determine where we are"""
    return Pose(
        x=p.x + v * cos(p.theta) * dt,
        y=p.y + v * sin(p.theta) * dt,
        theta=p.theta + omega * dt,
    )


def update_pose_icc(p: Pose, dt: float, v: float, omega: float) -> Pose:
    """ Update our position using the instantateous centure of curvature"""
    if isclose(omega, 0, abs_tol=1e-9):
        # In the case of linear motion we can actually take advantage of euler
        return update_pose_euler(p, dt, v, omega)
    else:
        R = v/omega
        new_x = p.x + R*(sin(p.theta + omega * dt) - sin(p.theta))
        new_y = p.y + R*(cos(p.theta) - cos(p.theta + omega * dt))
        new_theta = p.theta + omega*dt
        return Pose(new_x, new_y, new_theta)
