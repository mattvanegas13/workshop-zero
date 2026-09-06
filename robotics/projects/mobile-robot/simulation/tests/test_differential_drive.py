from ..differential_drive import inverse_kinematic, forward_kinematic
import pytest

class TestDifferentialDrive:
    @pytest.mark.parametrize(
        "v, omega , wheel_base, expected_wheel_velocities",
        [
            (1,0,1, lambda v_l, v_r: v_l==v_r), # Case 1: Linear motion 
            (0,1,1, lambda v_l, v_r: -v_l==v_r),# Case 2: Spin about center
            (1,.5,1,lambda v_l, v_r: v_r > v_l),# Case 3: Curvilinear/ arc'd motion
        ]
    )
    def test_inverse_kinematics(self, v, omega, wheel_base, expected_wheel_velocities ):
        assert expected_wheel_velocities(*inverse_kinematic(v, omega, wheel_base))
       
    def test_bijectivity_of_movement_functions(self):
        v_l_true, v_r_true = 1, 1
        v, w = forward_kinematic(v_l_true, v_r_true, 1)
        v_l, v_r = inverse_kinematic(v,w,1)       
        assert abs(v_l_true - v_l) < 1e-9 and abs(v_r_true - v_r) < 1e-9