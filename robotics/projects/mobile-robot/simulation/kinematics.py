"""
Responsible for the theoretical computation of robotics motion
"""
from typing import Tuple
from .pose import Pose, update_pose_icc


def inverse_kinematic(v: float, omega: float, wheel_base: float,) -> Tuple[float, float]:
    """ given v and omega return the inputs"""
    v_l = v - wheel_base / 2 * omega
    v_r = v + wheel_base / 2 * omega

    return v_l, v_r


def forward_kinematic(v_l: float, v_r: float, wheel_base: float,) -> Tuple[float, float]:
    """ given the inputs calculate v and omega"""
    v = (v_r + v_l) / 2
    omega = (v_r - v_l) / wheel_base

    return v, omega


def propagate_ground_truth(p: Pose, v_l: float, v_r: float, wheel_base: float, dt: float) -> Pose:
    """ Update the next ground truth for robot's pose to forward_kinematic """
    v, omega = forward_kinematic(v_l, v_r, wheel_base,)
    return update_pose_icc(p, dt, v, omega,)
