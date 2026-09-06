09/05/2026

This note comes from the design of our simple wheeled robot simulation
we have our pose_updating function 

```code
def update_pose_buggy(p:Pose, dt:float, v:float, omega:float) -> Pose:
    return Pose(
        x=p.x + v * cos(p.theta) * dt,
        y=p.y + v * sin(p.theta) * dt,
        theta=p.theta + omega * dt,
    )
```
Notice the case for Pose(1,1,1)
the subsequent update is (1,0,1) - which our sim would say that the 
bot moved in a line along the x - when in reality it should be doing an arc 

so how do we correct this.

Lets consider the Instantaneous Center of Curvature (ICC)

We can find the ICC

by taking the ratio of the linear speed and angular velocity we can find the radius of curvature.

Now suppose we have a robot at x, y, theta that moves at a constant v, and omega for dt
along some radius R - what is the ICC relative to that robots position, ( X_icc, Y_icc)

to find these cordinates we must first find the direction of the unit vector that points towards the ICC.
If we are traveling along r we can define a unit vector relative to the robot that dictates its direction - if we rotate it 90 degrees
we get the direction we are looking for

so cos(theta + pi/2) via the angle addtiion formula -> cos(theta)*cos(pi/2) - sin(theta)*sin(pi/2) = -sin(theta)
and sin(theta + pi/2) -> sin(theta)cos(pi/2) + cos(theta)sin(pi/2) = cos(theta)

so the vector that points to icc = R * (-sin(theta))x + cos(theta)y
or X_icc = x-Rsin(theta) and Y_icc = y+ R(cos(theta))
where x and y are the position of the robot

now going in reverse to update our position we have need to rearrange the terms leaving us

x = X_icc + Rsin(theta)
y = Y_icc - Rsin(theta)

great - now lets say we move along the circle then x preserves it form and can be found by
x = X_icc + Rsin(theta + dtheta)
y = Y_icc - Rcos(theta + dtheta)

substituting our definitions for X_icc
we can say 
x_new = x_old + R (sin(theta+dtheta)- sin(theta))
y_new = y_old + R (cost(theta) - cos(theta+dtheta))

recall that R is our radius of curvature we defined earlier so we can plug in v/w into our equation here

now if we compare the output of these inputs to the above two update rules we see that the new pose
according to euler = (1, 0, 1) 
and to the arc update = (sin(1), 1-cos(1), 1)

notice that there is an error that accumulates especially if we increase our angular velocity input. which beckons the following invesitagation

## Question
The question is how does the error change if the timestamp gets smaller

## Hypothesis
Well i would assume a smaller timestamp would have smaller error

## Setup
- v = 1.0 m/s
- omega = 0.5 rad/s
- T = 5 s
- dt = [1.0, 0.5, 0.1, 0.01]


## Data
- Final endpoint error - by just constructing the error vector and taking the magnitude
e_final = sqrt( (x_euler - x_arc_update) ** 2 + (x_euler - x_arc_update)**2 )
- trajectory error

## Results
dt         final error     RMSE           
1.00       0.952302        0.690057       
0.50       0.474905        0.326611       
0.10       0.094902        0.062399       
0.01       0.009490        0.006174 
## Interpretation
we can confirm our hypothesis to be correct - what is more interesting however it that is
roughly proportional - .5 is roughly half of the error we've accumulated by dt = 1

so why does this happen? It is because euler assumes that the robot maintains its heading for the duration of each timestep - the ICC model on the other hand accounts for the contious change in heading along the circular arc
## What I learned

