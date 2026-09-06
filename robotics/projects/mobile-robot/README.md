Defining abstraction boundary
what should our simulated robot expose as inputs and outputs

inputs - > desired v and w
outputs -> ground-truth position/pose, odometry reading, encoder ticks

the internal "black box" will be responsible for calcualting kinematics, velocities, encoder measurements 
