"""
What do different update rules say depending on the motion we travel?
Where do the rules break down?
"""

from math import sqrt
from ..pose import Pose, update_pose_euler, update_pose_icc


def endpoint_error(euler_pose: Pose, exact_pose: Pose) -> float:
    """ determine endpoint error using eucliden difference"""
    dx = euler_pose.x - exact_pose.x
    dy = euler_pose.y - exact_pose.y

    return sqrt(dx**2 + dy**2)


def trajectory_rmse(euler_poses: list[Pose], exact_poses: list[Pose],) -> float:
    """ root mean square error for our trajectories """
    squared_errors = []

    for euler_pose, exact_pose in zip(euler_poses, exact_poses):
        dx = euler_pose.x - exact_pose.x
        dy = euler_pose.y - exact_pose.y

        squared_errors.append(dx**2 + dy**2)

    return sqrt(sum(squared_errors) / len(squared_errors))


def run_experiment(v: float, omega: float, total_time: float, dt: float,):
    """ How do we deviate from what our position actually is using different update rules """
    num_steps = int(total_time / dt)

    euler_pose = Pose(0.0, 0.0, 0.0)
    icc_pose = Pose(0.0, 0.0, 0.0)

    euler_poses = []
    icc_poses = []

    for _ in range(num_steps):
        euler_pose = update_pose_euler(euler_pose, dt, v, omega)
        icc_pose = update_pose_icc(icc_pose, dt, v, omega)
        euler_poses.append(euler_pose)
        icc_poses.append(icc_pose)

    error = endpoint_error(euler_pose, icc_pose)
    root_means_square_error = trajectory_rmse(euler_poses, icc_poses,)

    return error, root_means_square_error


if __name__ == "__main__":
    V = 1.0
    OMEGA = 0.5
    TOTAL_TIME = 5.0

    timesteps = [1.0, 0.5, 0.1, 0.01, ]

    print(f"{'dt':<10} {'final error':<15} {'RMSE':<15}")

    for dt_i in timesteps:
        final_error, rmse = run_experiment(V, OMEGA, TOTAL_TIME, dt_i,)
        print(
            f"{dt_i:<10.2f} "
            f"{final_error:<15.6f} "
            f"{rmse:<15.6f}"
        )
