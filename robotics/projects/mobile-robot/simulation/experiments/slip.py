"""
What if our encoders are correct - but our wheels move in a way
that break our assumptions
"""
from ..sim import run_simulation
from ..robot_models import DifferentialDriveRobot, ConfigurationParam


def run_symetric_slip_scenario():
    """ 
    In this case we use our new class Wheel and define them with equivalent 
    tractions .9 - which indicates that for a given reading we actually move 
    less than we think we do 
    """
    c = ConfigurationParam(traction_l=.9, traction_r=.9)
    r = DifferentialDriveRobot(c)
    result = run_simulation(
        r,
        v_l=0.5,
        v_r=0.5,
        dt=0.01,
        total_time=5.0,
    )

    print(
        f"position_error={result['position_error']:.6f} | "
        f"heading_error={result['heading_error']:.6f} | "
        f"odom={result['odometry_pose']} | "
        f"truth={result['ground_truth_pose']}"
    )

    return result

    # position_error=0.250000 |
    # heading_error=0.000000 |
    # odom=Pose(x=2.5, y=0.0, theta=0.0) |
    # truth=Pose(x=2.250000000000021, y=0.0, theta=0.0)
    #
    # As we can see in the case of symmetric slippage
    # the odometry does over estimate the forward distance
    # and since both wheels slip equally - we agree on theta


def run_asymetric_slip_scenario():
    """ 
    In this case one of the wheels slips at a differen rate 
    - which logic states that we should see a slide/discrepancy in theta
    """
    c = ConfigurationParam(traction_l=.9, traction_r=1)
    r = DifferentialDriveRobot(c)
    result = run_simulation(
        r,
        v_l=0.5,
        v_r=0.5,
        dt=0.01,
        total_time=5.0,
    )

    print(
        f"position_error={result['position_error']:.6f} | "
        f"heading_error={result['heading_error']:.6f} | "
        f"odom={result['odometry_pose']} | "
        f"truth={result['ground_truth_pose']}"
    )

    return result
    # position_error=0.622680 |
    # heading_error=0.500000 |
    # odom=Pose(x=2.5, y=0.0, theta=0.0) |
    # truth=Pose(x=2.277271308369995, y=0.5814828310207469, theta=0.5000000000000066)
    #
    # and it seems that there is now both an error in the forward distance traveled
    # as well as the expected heading


if __name__ == "__main__":
    run_asymetric_slip_scenario()
