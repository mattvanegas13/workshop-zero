"""
A pseudo model of encoders our robots will have
"""

from dataclasses import dataclass
from math import pi, trunc


@dataclass
class EncoderReading:
    """ Data Object that contains data we get from our encoder """
    delta_ticks: float
    ticks_per_revolution: int

    def angular_displacement(self) -> float:
        """ What it says on the tin"""
        return (2 * pi * self.delta_ticks / self.ticks_per_revolution)


class Encoder:
    """
    Ideal encoder.

    Allows fractional tick measurements.
    """

    def __init__(self, ticks_per_revolution: int,) -> None:
        self.ticks_per_revolution = ticks_per_revolution

    def reset(self):
        """zero out the encoder data"""

    def delta_ticks(self, angular_velocity: float, dt: float,) -> float:
        """ Calculates how many ticks the encoder would see """
        angular_displacement = angular_velocity * dt
        revolutions = angular_displacement / (2*pi)
        return self.ticks_per_revolution * revolutions

    def read(self, v_wheel: float, dt: float,) -> EncoderReading:
        """ Emits a reading """
        return EncoderReading(
            delta_ticks=self.delta_ticks(v_wheel, dt),
            ticks_per_revolution=self.ticks_per_revolution,
        )


class QuantizedEncoder(Encoder):
    """
    Encoder that emits only complete ticks.

    Fractional wheel rotation is retained internally
    until enough motion accumulates to cross another
    encoder tick.
    """

    def __init__(self, ticks_per_revolution: int) -> None:
        super().__init__(ticks_per_revolution)
        self.residual_ticks = 0

    def reset(self) -> None:
        """ set the amount of residual ticks we have in our quantized encoder back to zero """
        self.residual_ticks = 0.0

    def delta_ticks(self, angular_velocity: float, dt: float,) -> int:
        ideal_delta_ticks = super().delta_ticks(angular_velocity, dt)
        available_ticks = self.residual_ticks + ideal_delta_ticks
        emitted_ticks = trunc(available_ticks)
        self.residual_ticks = available_ticks - emitted_ticks
        return emitted_ticks
