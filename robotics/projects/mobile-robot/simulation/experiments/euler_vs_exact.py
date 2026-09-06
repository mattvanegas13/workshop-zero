from math import sqrt
from ..differential_drive import (
    Pose,
    update_pose_euler,
    update_pose_icc
)


def endpoint_error(euler_pose: Pose, exact_pose: Pose) -> float:
    dx = euler_pose.x - exact_pose.x
    dy = euler_pose.y - exact_pose.y

    return sqrt(dx**2 + dy**2)


def trajectory_rmse(
    euler_poses: list[Pose],
    exact_poses: list[Pose],
) -> float:

    squared_errors = []

    for euler_pose, exact_pose in zip(euler_poses, exact_poses):
        dx = euler_pose.x - exact_pose.x
        dy = euler_pose.y - exact_pose.y

        squared_errors.append(dx**2 + dy**2)

    return sqrt(sum(squared_errors) / len(squared_errors))


def run_experiment(
    v: float,
    omega: float,
    total_time: float,
    dt: float,
):
    num_steps = int(total_time / dt)

    euler_pose = Pose(0.0, 0.0, 0.0)
    icc_pose = Pose(0.0, 0.0, 0.0)

    euler_poses = []
    icc_poses = []

    for _ in range(num_steps):
        euler_pose = update_pose_euler(
            euler_pose,
            dt,
            v,
            omega,
        )

        icc_pose = update_pose_icc(
            icc_pose,
            dt,
            v,
            omega,
        )

        euler_poses.append(euler_pose)
        icc_poses.append(icc_pose)

    final_error = endpoint_error(euler_pose, icc_pose)

    rmse = trajectory_rmse(
        euler_poses,
        icc_poses,
    )

    return final_error, rmse


if __name__ == "__main__":
    v = 1.0
    omega = 0.5
    total_time = 5.0

    timesteps = [
        1.0,
        0.5,
        0.1,
        0.01,
    ]

    print(f"{'dt':<10} {'final error':<15} {'RMSE':<15}")

    for dt in timesteps:
        final_error, rmse = run_experiment(
            v,
            omega,
            total_time,
            dt,
        )

        print(
            f"{dt:<10.2f} "
            f"{final_error:<15.6f} "
            f"{rmse:<15.6f}"
        )