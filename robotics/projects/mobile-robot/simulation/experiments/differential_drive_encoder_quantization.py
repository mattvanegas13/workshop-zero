"""
File where we run our simulations for a differential drive robot
"""

from typing import List
from ..robot_models import ConfigurationParam, DifferentialDriveRobot
from ..encoders import QuantizedEncoder
from ..sim import run_simulation


def _run_differential_drive_simulation(robot: DifferentialDriveRobot, dts: List[float]):
    results = []
    for dt in dts:
        result = run_simulation(robot, v_l=0.5, v_r=1.0,
                                dt=dt, total_time=5.0)
        results.append(result)
        print(
            f"encoder={type(robot.left_encoder).__name__} | "
            f"tpr={robot.config.ticks_per_revolution} | "
            f"wheel_radius={robot.config.r_r} | "
            f"wheel_base={robot.config.wheel_base} | "
            f"dt={dt} | "
            f"position_error={result['position_error']:.10f} | "
            f"heading_error={result['heading_error']:.10f}"
        )
    return results


DTS = [0.5, 0.1, 0.05, 0.01]
ideal_encoder_sim_run = _run_differential_drive_simulation(
    DifferentialDriveRobot(), DTS
)
quantized_encoder_sim_run = _run_differential_drive_simulation(
    DifferentialDriveRobot(encoder_type=QuantizedEncoder), DTS
)


def vary_ticks_per_revolution():
    """
    The point of this function is to test our hypothesis that upon increasing the number of 
    ticks per revolution - we would expect the dead reckoning error to decrease.
    Why? Because more ticks per revolution increases the resolution of the encoder.
    i.e one tick corresponds to a smaller wheel rotation - so we tick out more times
    and thus we get smaller delta_s
    """
    ticks_per_revolution = [720]
    wheel_radius = 0.1
    wheel_base = 0.5
    for tick_resolution in ticks_per_revolution:
        c = ConfigurationParam(wheel_radius, wheel_base, tick_resolution)
        r = DifferentialDriveRobot(c, encoder_type=QuantizedEncoder)
        _run_differential_drive_simulation(r, [.01])

#     Results are:
#     | TPR | Position error | Heading error |
#     | --: | -------------: | ------------: |
#     |  90 |      0.0037901 |     0.0013770 |
#     | 180 |      0.0017969 |     0.0013770 |
#     | 360 |      0.0009257 |     0.0013770 |
#     | 720 |      0.0005174 |     0.0003683 |
# |

#     so what does this mean?
#     Overall it seems like both position and heading error generally
#     decrease as we increase the resolution of a given encoder

#     doubling the encoder esolution is roughly equivalent to a 2x reduction in position
#     error at each time - the dominant error here is behavir like
#     e_pos proportional to 1 / N
#     where N is ticks per revolution
#     thus substantially decreasing positional and rottaional odometry error


if __name__ == "__main__":
    vary_ticks_per_revolution()
