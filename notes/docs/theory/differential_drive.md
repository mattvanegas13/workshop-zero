# Differential Drive Kinematics

## 1. Assumptions
- Rigid robot body
- Two standard wheels
- Wheel radius: `r`
- Distance between wheels: `L`
- No lateral slip
- Pure rolling at the wheel-ground contact
- Robot body frame has forward velocity `v` and yaw rate `ω`

## 2. Wheel Variables

Left/right wheel angular velocities:

$$
\dot{\phi}_L,\quad \dot{\phi}_R
$$

Wheel linear velocities:

$$
v_L = r\dot{\phi}_L
$$

$$
v_R = r\dot{\phi}_R
$$

## 3. Important Distinction

`ω = \dot{\theta}` is the yaw rate of the entire robot.

`\dot{\phi}_L` and `\dot{\phi}_R` are the angular velocities of the individual wheels.

## 4. Straight-Line Motion

If

$$
v_L = v_R
$$

then

$$
\omega = 0
$$

and

$$
v = v_L = v_R.
$$

This motivates the general forward-velocity equation:

$$
v = \frac{v_L + v_R}{2}.
$$

## 5. Pure Rotation

For rotation about the robot midpoint:

$$
v_R = \omega\frac{L}{2}
$$

$$
v_L = -\omega\frac{L}{2}
$$

Therefore:

$$
v_R - v_L = \omega L
$$

so

$$
\omega = \frac{v_R-v_L}{L}.
$$

## 6. General Differential-Drive Model

$$
v = \frac{v_R+v_L}{2}
$$

$$
\omega = \frac{v_R-v_L}{L}
$$

Substituting wheel angular velocities:

$$
v =
\frac{r}{2}
\left(
\dot{\phi}_R+\dot{\phi}_L
\right)
$$

$$
\omega =
\frac{r}{L}
\left(
\dot{\phi}_R-\dot{\phi}_L
\right)
$$

## 7. Instantaneous Center of Curvature

If the robot turns around an ICC at radius `R`:

$$
v = \omega R
$$

The wheels travel around radii:

$$
R_L = R-\frac{L}{2}
$$

$$
R_R = R+\frac{L}{2}
$$

Therefore:

$$
v_L = \omega\left(R-\frac{L}{2}\right)
$$

$$
v_R = \omega\left(R+\frac{L}{2}\right)
$$

and:

$$
R =
\frac{L}{2}
\frac{v_R+v_L}{v_R-v_L}.
$$

Sanity checks:

- `v_R = v_L` → `R → ∞` → straight line
- `v_R = -v_L` → `R = 0` → rotation in place

## 8. Body Frame to World Frame

The differential-drive robot has body-frame velocity:

$$
\begin{bmatrix}
v\\
0
\end{bmatrix}
$$

Rotating into the world frame gives:

$$
\dot{x}=v\cos\theta
$$

$$
\dot{y}=v\sin\theta
$$

$$
\dot{\theta}=\omega.
$$

Therefore:

$$
\dot{x}
=
\frac{v_R+v_L}{2}\cos\theta
$$

$$
\dot{y}
=
\frac{v_R+v_L}{2}\sin\theta
$$

$$
\dot{\theta}
=
\frac{v_R-v_L}{L}.
$$

## 9. Discrete Odometry

Using a timestep `Δt`:

$$
x_{k+1}
=
x_k+v\cos\theta_k\Delta t
$$

$$
y_{k+1}
=
y_k+v\sin\theta_k\Delta t
$$

$$
\theta_{k+1}
=
\theta_k+\omega\Delta t.
$$

This is forward Euler integration.

## 10. Encoder Form

For wheel displacement:

$$
\Delta s_L=r\Delta\phi_L
$$

$$
\Delta s_R=r\Delta\phi_R
$$

Robot displacement:

$$
\Delta s=
\frac{\Delta s_R+\Delta s_L}{2}
$$

Robot heading change:

$$
\Delta\theta=
\frac{\Delta s_R-\Delta s_L}{L}.
$$

If the encoder provides `N` ticks per revolution:

$$
\Delta\phi =
2\pi\frac{\Delta n}{N}
$$

so:

$$
\Delta s =
2\pi r\frac{\Delta n}{N}.
$$

## 11. What I Learned

- Wheel spin is not the same thing as robot yaw rate.
- The average wheel velocity controls forward motion.
- The difference in wheel velocity controls rotation.
- Differential drive is nonholonomic because it cannot instantaneously move sideways.
  - nonholonomic being defined as system, function, or constraint that do not just depend on position to be derivable (it needs velocities or path needed to reach a state )
- Encoder measurements can be integrated to estimate robot pose.

## 12. Open Questions

- How much error does Euler integration introduce while turning?
- How do encoder resolution and wheel radius affect odometry accuracy?
- How does wheel slip corrupt the estimate?
- How should odometry be represented in ROS 2?
- What does `tf2` need from the robot?
