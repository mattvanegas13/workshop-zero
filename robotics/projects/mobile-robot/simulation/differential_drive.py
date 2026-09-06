from typing import Tuple, List
from math import sin, cos, isclose 
from dataclasses import dataclass

@dataclass
class Pose:
    x: float
    y: float
    theta: float

def inverse_kinematic(v: float, omega:float, wheel_base:float) -> Tuple[float, float]:
    v_l = v - wheel_base/2 * omega
    v_r = v + wheel_base/2 * omega
    return v_l, v_r

def forward_kinematic(v_l:float, v_r:float, wheel_base) -> Tuple[float, float]:
    v = (v_r + v_l) / 2
    omega = (v_r - v_l)/ wheel_base
    return v, omega

def update_pose_euler(p:Pose, dt:float, v:float, omega:float) -> Pose:
    return Pose(
        x=p.x + v * cos(p.theta) * dt,
        y=p.y + v * sin(p.theta) * dt,
        theta=p.theta + omega * dt,
    )
    
def update_pose_icc( p:Pose, dt:float, v:float, omega:float) -> Pose:
    if isclose(omega, 0, abs_tol=1e-9):
        # In the case of linear motion we can actually take advantage of euler 
        return update_pose_euler(p, dt, v, omega)
    else:
        R = v/omega
        new_x = p.x + R*(sin(p.theta + omega * dt) - sin(p.theta))
        new_y = p.y + R*(cos(p.theta) - cos(p.theta + omega * dt))
        new_theta = p.theta + omega*dt
        return Pose(new_x, new_y, new_theta)