"""
Unit tests -
"""
from math import isclose, pi
import pytest
from ..kinematics import inverse_kinematic, forward_kinematic
from ..encoders import EncoderReading
from ..odometry import odometry_update
from ..pose import Pose


class Test:
    @pytest.mark.parametrize(
        "v, omega , wheel_base, expected_wheel_velocities",
        [
            (1, 0, 1, lambda v_l, v_r: v_l == v_r),  # Case 1: Linear motion
            (0, 1, 1, lambda v_l, v_r: -v_l == v_r),  # Case 2: Spin about center
            # Case 3: Curvilinear/ arc'd motion
            (1, .5, 1, lambda v_l, v_r: v_r > v_l),
        ]
    )
    def test_inverse_kinematics(self, v, omega, wheel_base, expected_wheel_velocities):
        """ Input -> robot behavior"""
        assert expected_wheel_velocities(
            *inverse_kinematic(v, omega, wheel_base))

    def test_bijectivity_of_movement_functions(self):
        """ F and F^{-1} work"""
        v_l_true, v_r_true = 1, 1
        v, w = forward_kinematic(v_l_true, v_r_true, 1)
        v_l, v_r = inverse_kinematic(v, w, 1)
        assert abs(v_l_true - v_l) < 1e-9 and abs(v_r_true - v_r) < 1e-9
