# Question

How does our odometry calculation vary when we introduce traction loss into the simulation?

# Hypothesis

When wheel traction is reduced, encoder measurements will indicate more wheel motion than is actually transferred to the ground. As a result, odometry will overestimate the robot's traveled distance.

If both wheels experience equal traction loss, position error should increase while heading remains approximately correct.

If the left and right wheels experience different traction, the true robot will follow a curved trajectory even though odometry may report straight-line motion.

# Method

Introduce a `Wheel` abstraction containing a traction parameter.

The encoder continues to measure the full wheel rotation, while the ground-truth motion uses the traction-adjusted wheel velocity.

Run two experiments:

1. **Symmetric slip:** both wheels use traction = 0.9.
2. **Asymmetric slip:** one wheel uses traction = 0.9 while the other uses traction = 1.0.

Compare the true pose against the pose reconstructed from encoder odometry.

# Results

See `simulation.experiments.slip.py`.

For symmetric slip:

* Position error: 0.25 m
* Heading error: 0
* Odometry pose: `(2.5, 0.0, 0.0)`
* True pose: approximately `(2.25, 0.0, 0.0)`

For asymmetric slip:

* Position error: approximately 0.623 m
* Heading error: 0.5 rad
* Odometry pose: `(2.5, 0.0, 0.0)`
* True pose: approximately `(2.277, 0.581, 0.5)`

# Interpretation

**Symmetric slip → distance error without heading error.**

When both wheels lose the same fraction of traction, the robot still travels straight, but the encoders report more motion than is actually transferred to the ground. Odometry therefore overestimates forward distance.

**Asymmetric slip → both position and heading error.**

When traction differs between the wheels, their actual ground velocities differ even though the encoders may report equal wheel motion. The physical robot therefore follows a curved path while odometry can incorrectly report straight-line travel.

This demonstrates an important limitation of wheel odometry: encoder measurements can accurately describe wheel rotation while still failing to describe the robot's true motion relative to the ground.

# Limitations

* Slip is modeled using a constant traction multiplier.
* No stochastic or time-varying slip is modeled.
* Terrain and dynamic effects are excluded.
* Encoder quantization and calibration error are not combined with slip in this experiment.

# Next Experiment

Move from passive pose estimation to closed-loop control: use feedback to make the robot correct deviations from a desired state rather than only estimating its motion.


