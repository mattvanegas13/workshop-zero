"""
What happens if we have some sort of calibration error in our robot?

Suppose we have a robot who's wheels have radius = .1
but our odometry believes that radius = .101
"""
from ..robot_models import DifferentialDriveRobot, ConfigurationParam
from ..sim import run_simulation_systematic_calibration_error
from pprint import pprint


def symmetric_calibration_error_symetric_mismatch():
    """
    In this case - if our odometry believes that each radius is actually .101
    we can roughly expect to see the following scale factor:
    let k = r_odometry/ r_true
    then del_sr_hat = k * del_s and del_sr_hat = k * del_r
    from our previous equation
    del_s_hat = del_sr_hat + del_sl_hat / 2 => k (del_s + del_r)/ 2
    or del_s_hat = k * del_s
    """

    # Lets define a robot with nominal r_l, r_r, L
    # and one with the odometry assumed params r^_L, r^_R, L^
    nonimal_config = ConfigurationParam(r_l=.1, r_r=.1, wheel_base=.5)
    odometry_assumed_config = ConfigurationParam(
        r_l=.105, r_r=.105, wheel_base=.5)
    # We use the ideal encoder to prevent having two effects from contributing to the
    # measured pose error
    robot_with_nominal_configs = DifferentialDriveRobot(nonimal_config)
    assumed_odomtery_robot = DifferentialDriveRobot(odometry_assumed_config)
    results = run_simulation_systematic_calibration_error(
        true_robot=robot_with_nominal_configs,
        odom_model_robot=assumed_odomtery_robot,
        v_l=.5,
        v_r=1.0,
        dt=.01,
        total_time=5.0
    )
    pprint(results)

    # {'dt': 0.01,
    #  'odometry_model_pose': Pose(x=-0.6442038293771704,
    #                              y=0.36593757309200176,
    #                              theta=5.250000000000098),
    #  'true_robot_pose': Pose(x=-0.7191932059973529,
    #                          y=0.5372533609025792,
    #                          theta=5.0),
    #
    # So it seems true heading ends at 5 but the odom model says 5.25
    # which implies the that the +5% radius bias produced a 5% heading bias just as we
    # postulated. however this isn't quite the case for the x and y positions
    # in this case what scaled by 5% was the inferred wheel distances
    # which checks out with what we established


def mismatched_wheel_radii():
    """ In this case what occurs if there is a non-symetric mismatch in the radii """
    # Same set up although in this case we let v_l = v_r
    # the nominal robot should be going straight
    # but if theres a mismatch of radii in
    nonimal_config = ConfigurationParam(r_l=.1, r_r=.1, wheel_base=.5)
    odometry_assumed_config = ConfigurationParam(
        r_l=.095, r_r=.105, wheel_base=.5)
    robot_with_nominal_configs = DifferentialDriveRobot(nonimal_config)
    assumed_odomtery_robot = DifferentialDriveRobot(odometry_assumed_config)
    results = run_simulation_systematic_calibration_error(
        true_robot=robot_with_nominal_configs,
        odom_model_robot=assumed_odomtery_robot,
        v_l=.5,
        v_r=.5,
        dt=.01,
        total_time=5.0
    )
    pprint(results)
    # {'dt': 0.01,
    #  'odometry_model_pose': Pose(x=2.397127792901367,
    #                              y=0.612087216051786,
    #                              theta=0.5000000000000066),
    #  'true_robot_pose': Pose(x=2.5, y=0.0, theta=0.0)}
    # we see in this case we think we veer off slightly toward +y


def mismatch_wheel_base():
    """
    Now what if we tweak the wheel_base of the robot?
    prediction: if wheel base its shorter the odom model will think 
    the heading has changed much faster than what it actually has. in other words
    it thinks it turns sharper
    """
    nonimal_config = ConfigurationParam(r_l=.1, r_r=.1, wheel_base=.5)
    odometry_assumed_config = ConfigurationParam(
        r_l=.1, r_r=.1, wheel_base=.525)
    robot_with_nominal_configs = DifferentialDriveRobot(nonimal_config)
    assumed_odomtery_robot = DifferentialDriveRobot(odometry_assumed_config)
    results = run_simulation_systematic_calibration_error(
        true_robot=robot_with_nominal_configs,
        odom_model_robot=assumed_odomtery_robot,
        v_l=.5,
        v_r=1.0,
        dt=.01,
        total_time=5.0
    )
    pprint(results)
    # turns out we were right
    # {'dt': 0.01,
    #  'odometry_model_pose': Pose(x=-0.7865377685640663,
    #                              y=0.7485250831880265,
    #                              theta=4.761904761904807),
    #  'true_robot_pose': Pose(x=-0.7191932059973529,
    #                          y=0.5372533609025792,
    #                          theta=5.0)}


if __name__ == "__main__":
    mismatch_wheel_base()
