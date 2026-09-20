"""
Bits and pieces that are responsible for running the simulation for mobile robot
"""
from math import sqrt
from .pose import Pose
from .robot_models import DifferentialDriveRobot, MobileRobot


def position_error(ground_truth: Pose, odometry: Pose,) -> float:
    """ Responsible for computing position deviation """
    return sqrt((odometry.x - ground_truth.x) ** 2 + (odometry.y - ground_truth.y) ** 2)


def heading_error(ground_truth: Pose, odometry: Pose,) -> float:
    """ Responsible for computing heading deviation """
    return abs(odometry.theta - ground_truth.theta)


def run_simulation(robot: MobileRobot, v_l: float, v_r: float, dt: float, total_time: float):
    """ Takes in a robot and inputs and runs a simulation for total_time with dt time segments"""
    # Critical for stateful sensors such as
    # QuantizedEncoder.
    robot.reset()
    ground_truth_pose = Pose(0.0, 0.0, 0.0,)
    odometry_pose = Pose(0.0, 0.0, 0.0,)
    ground_truth_history = [ground_truth_pose]
    odometry_history = [odometry_pose]
    elapsed_time = 0.0

    while elapsed_time < total_time:

        step_dt = min(dt, total_time - elapsed_time)

        # Actual simulated robot motion
        ground_truth_pose = robot.ground_truth_step(
            ground_truth_pose, v_l, v_r, step_dt
        )

        # Sensors observe that wheel motion
        wheel_data = robot.sensor_step(v_l, v_r, step_dt)

        # Pose estimated using sensor measurements
        odometry_pose = robot.odometry_step(odometry_pose, wheel_data)

        ground_truth_history.append(ground_truth_pose)
        odometry_history.append(odometry_pose)

        elapsed_time += step_dt

    return {
        "dt": dt,
        "ground_truth_pose": ground_truth_pose,
        "odometry_pose": odometry_pose,
        "position_error": position_error(
            ground_truth_pose,
            odometry_pose,
        ),
        "heading_error": heading_error(
            ground_truth_pose,
            odometry_pose,
        ),
        "ground_truth_history":
            ground_truth_history,
        "odometry_history":
            odometry_history,
    }


def run_simulation_systematic_calibration_error(
        true_robot: MobileRobot, odom_model_robot: MobileRobot,
        v_l: float, v_r: float, dt: float, total_time: float):
    """
    Take in a robot with a given nominal radii for its wheel
    and one whose odometry believe it is different from the nominal radii
    If we run them from the same starting pose and give them identical inputs
    how does the systematic error from the odom mis-perception contribute to the robots
    position and heading error 
    """
    true_robot.reset()
    odom_model_robot.reset()
    true_robot_pose = Pose(0.0, 0.0, 0.0,)
    odom_model_robot_pose = Pose(0.0, 0.0, 0.0,)
    true_robot_pose_history = [true_robot_pose]
    odom_model_robot_pose_history = [odom_model_robot_pose]
    elapsed_time = 0.0

    while elapsed_time < total_time:
        # move the robot
        time_step = min(dt, total_time - elapsed_time)
        true_robot_pose = true_robot.ground_truth_step(
            true_robot_pose, v_l, v_r, time_step)

        # what the sensor sees based off the inputs
        # raw measurement produced by the real robot
        sensor_data = true_robot.sensor_step(v_l, v_r, time_step)

        # then we feed what the sensor on the true robot saw
        # to the odom model to see how far we have traveled based on odometry model's geometry
        odom_model_robot_pose = odom_model_robot.odometry_step(
            odom_model_robot_pose, sensor_data)

        true_robot_pose_history.append(true_robot_pose)
        odom_model_robot_pose_history.append(odom_model_robot_pose)

        elapsed_time += dt

    return {
        "dt": dt,
        "true_robot_pose": true_robot_pose,
        "odometry_model_pose": odom_model_robot_pose,
        # "true_robot_pose_history":
        #     true_robot_pose_history,
        # "odometry_model_pose_history":
        #     odom_model_robot_pose_history,
    }
