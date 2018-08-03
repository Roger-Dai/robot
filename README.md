# Robot Control

The goal of this project is to communicate with the UR5 Robot arm through a Python script, which would later be turned into a C++ program that can be incorporated into the main MobileLighting app. The C++ program is not included in this repository since it is included here in the main program: https://github.com/nmosier/MobileLighting/tree/master/MobileLighting_Mac/RobotControl/RobotControl. All the control commands that is useful for the program are all included in the RobotControls.py program. This repository also includes the program PathMovements.py, which includes some pre-recorded trajectories. These trajectories were recorded throughout the project to test the program.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

You should have Python 3 running on your computer in order to execute this program. 

In order to instruct the robot arm through this program and see the effect, a UR robot arm needs to be connected to the Internet and have a fixed IP address. 

You also need a flashdrive that could transport files from your computer to the UR robot arm controller.

### Installing and Configuring

You simply need to clone this repository to your local directory. No further installations are required.

Before you can successfully communicate with the robot, you have to do the following to set up.

1. Find out the fixed IP address of your robot arm. Open the Python program you wish to use, and change the "HOST" global variable at the top of the program. 

2. Find out the IP address of your own computer. Open the file communicate.script, find the line below and change IP address to that of your own computer. 

```
connected = socket_open("140.223.162.184", 30000, "pos")
```

3. Use your flashdrive to transport the file communicate.script to the robot controller. Then create an empty program called *communicate.urp* on the robot arm, and add the script to the program.

Now you are reading to run the program.

## Running the program

There are two Python programs that could be executed in this folder. 

RobotControls.py includes all the control commands that instruct the robot arm to carry out tasks. **You should run this program if you are recording a trajectroy for the MobileLighting app.** The command to run the program is the following:

```
python3 RobotControls.py (-c|-n)
```
-c: Establish a two-way connection with the robot arm. The program can both send and receive information from the robot arm.

-n: Establish a one-way connection with the robot arm. The program can only send instructions to the robot arm.

After a connection is established, the program would print out a statement confirming so and stating which type of connection is established.

**If you wish to use the -c option, you also need to have the program *communicate.urp* running on the robot controller at the same time.** Once a two-way connection is successfully established, the Python program would print out a statement, and the robot controller would also pop up a window saying so.

PathMovements.py includes some pre-recorded trajectories and the commands to move the robot arm along the trajectories. The command to run the program is the following and no arguments are needed:

```
python3 PathMovements.py
```

## Using the program

After the connections are established, the programs would prompt "Enter command: " and you can enter different commands to instruct the robot arm.

1. Below is a list of all commands included in the program *RobotControls.py* and their explanations. You can also have this list printed if you type "help" at the prompt "Enter command: ".

    - help: Get a list of all commands and what they do
    - done: Terminate all the connections and the program
    - powerdown: Shut down the robot arm remotely
    - freedrive: Put the robot arm into free drive mode
    - end freedrive: End the free drive mode on the robot arm
    - pose: Get the pose data from the robot arm
    - joints: Get the joint positions of the current robot arm configuration, both in degrees and radians
    - move pose: Move the robot arm to a certain pose with certain velocity and acceleration. The program would first ask for the acceleration(m/s^2) and velocity(m/s), and then the pose with six numbers separated by commas.
    - move joints: Move the robot arm to a certain joint position with certain velocity and acceleration. The program would first ask for the acceleration(m/s^2) and velocity(m/s), and then the joint position with six numbers separated by commas.
    - linear-x: Move the robot arm strictly along the x-axis for a certain distance. The program would first ask for the acceleration(m/s^2) and velocity(m/s), and then the distance(m) along the x-axis you want the robot arm to move. **The axes here are determined by the base reference frame**.
    - linear-y: Move the robot arm strictly along the y-axis for a certain distance. The program would first ask for the acceleration(m/s^2) and velocity(m/s), and then the distance(m) along the y-axis you want the robot arm to move. **The axes here are determined by the base reference frame**.
    - linear-z: Move the robot arm strictly along the z-axis for a certain distance. The program would first ask for the acceleration(m/s^2) and velocity(m/s), and then the distance(m) along the z-axis you want the robot arm to move. **The axes here are determined by the base reference frame**.

2. Below is a list of all commands included in the program *PathMovements.py* and their explanations. You can also have this list printed if you type "help" at the prompt "Enter command: ".

    - help: Get a list of all commands and what they do
    - done: Terminate all the connections and the program
    - powerdown: Shut down the robot arm remotely
    - square: Move the robot arm around in a pre-recorded square on the horizontal plane
    - star: Move the robot arm around in a pre-recorded star shape on the vertical plane
    - arc: Move the robot arm around in a pre-recorded arc
    - curve: Move the robot arm around in a pre-recorded square on the horizontal plane continuously with smoothed out edges
    - arm: Move the robot arm around in a pre-recorded arc that scans a scene

### Understanding the communication with the robot arm

The program talks to the robot arm through sockets. The robot arm controller hosts different ports. Port 30000 is used to establish a server connection which allows the robot arm to send specific information through the program on the robot controller. Port 30001 and 30002 can be used to establish a client connection which allows the Python program to send strings to the robot arm. The robot arm the interprets the strings as URScript commands. **All commands must be followed by an end-of-line symbol "\n".** You can either send one line instructions or functions. You cannot send instructions of multiple lines without wrapping them in a function first. Included in this repository, there is also official documentation for the URScript language. 

#### Notes

The different move functions such as movej() and movel() are the most commonly used ones in the program. The r argument for these functions stands for blend radius and enables the robot to do a smooth motion instead of stopping at each waypoint. The t argument of these functions is the total time it would take to complete the movement. **This could be used to help automating the MobileLighting app.** This way the user does not have to hit enter to tell the program the robot arm is in position since we know exactly how long it would take.

### How to record a trajectory for the MobileLighting app

1. Start the communicate.urp program on the robot controller.

2. Run the RobotControls.py program on the computer.

3. Set the robot arm in free drive mode by typing in "freedrive".

4. Move the robot arm to a desired position and type in "pose" to get the pose data.

5. Repeat step 4 until you have all the points you need.

6. Copy and paste the different poses you got to the file trajectory.yml generated by the application.

7. Terminate the program by typing in "done".

## Author

* **Roger Dai**

## Acknowledgments

* Thanks to Professor Daniel Scharstein from Middlebury College for overseeing this project.
