Question:
How does our calculation for  position change if our there is a systematic mismatch in our robots geometry differs 
from what it actually is

Hypothesis:
Depending on the geometric mismatch, the robot's trajectory will be systematically under- or over-estimated.

For a common multiplicative error in both wheel radii, we expect inferred wheel displacement and heading change to scale proportionally with the radius error.

For asymmetric wheel-radius errors or wheelbase errors, we expect different systematic distortions in the reconstructed trajectory.

Method:
- we first induce a symmetric mismatch in wheel radii as perceived by the encoder - where we believe that both wheels are 
larger than what they are

- a second trial that has an asymetric mismatch in radii

- variation in the wheel base ( or distance between the wheels

Results:
- see the file differenntial_drive_param_mismatch

Interpretation:
common wheel-radius bias → scales inferred travel and heading
left/right radius mismatch → creates false curvature
wheelbase bias → systematically over/underestimates heading change


Next expiramenource: what happens in the case of slippage with our odometry calculation
