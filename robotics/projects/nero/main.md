# About
Nero, or the Neil Rover, is my attempt at an autonomous/ teleoperated driven rover used in a domestic setting. Its origins stem from the byproduct of circumstance - our old roomate, Neil, has left our abode to find more stimulating intellectual pursuits in the bay. However we would love for him to still be here in spirit - which would be more easily achieved if we made him a mechanical vessel. 


# Design Story
I've gone back and forth about how to go about crafting the vessel we will summon neil to. Originally a bipedal humanoid seems the closest to the original flesh counterpart however I decided to start as simple as possible - a small quadri-wheeled robot who is to be iterated and improved upon as our budget and creativity allow.

## Base form and first steps
The simplest mile stone for this project starts with a four wheeled robot that can be controlled via a web server. No Intelligence thus far - just the mobile chassis. Which means there are two pieces to this puzzle - the IoT communication Hub - and the chassis


### IoT communication interface
So we have a couple of ways to go about this - below will be a set of approaches and at the end we will choose one based on ease of implementation and reduction of latency ( we want the person operating the robot to be able to do so in near realtime ). But before we begin designs we need to establish what data exactly needs to be communicated ( at least whats necessary for this stage of the project ) 

#### From User to Bot
- Rotational commands
- Translational commands 

#### From Bot to User
- Video Feed of what the robot sees 
- Acknowledgement of the movement commands? In other words - ack that we have received the request to move foward for example/ or if its unable to?

So with that out of the way what design minimizes latency communcation?

#### IoT system design
- A single rasperry pi
    - we can run the webserver on the pi and translate the commands we recieve directly to the actuators
    - The problem with this is that I'm not sure if the raspberry can handle:
        - video streaming
        - actuacion of motor for the wheels
        - web server that acts as the comms hub between users and the bot

- an esp32 with a websocket connection to the raspberry pi webserver ( which this may be the better idea since we can physically seperate the two entities this way and ajust/upgrade either as needed)
    - only issue is that we basically introduce another layer for incoming messages which could be an issue wrt to latency
    - a benefit however is that this will also allow us to build a queue storage systems for movement commnands. What happens if the user disconnects/ connection drops during operation? how do we manage idempotancy in this context?

- incoporate predictive moments to help calc time

#### Linking Robotics Kinematics