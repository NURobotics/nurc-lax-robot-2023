import sys
sys.path.append("/Users/samuelhodge/GitHub/nurc-lax-robot-2023/motor_control")
from PyRoboteq import roboteq_commands as cmds
from motor_controller import Controller
import time
import numpy as np
import matplotlib.pyplot as plt

# Written by Sam Hodge
# Updated Spring 2023

# Code to test how quickly the robotec motor controller can handle new commands.
# Values must be in the range of X:[-1,1], Y:[-0.8,0.8] meters

# Create arrays with trajectory circle of radius 0.6

# X = 0.6 * cos(theta)
# Y = 0.6 * sin(theta)

controller = Controller(debug_mode = False, exit_on_interrupt = False)  # Create the controller object
is_connected = controller.connect("/dev/tty.usbmodemC13E847AFFFF1") # connect to the controller (COM9 for windows, /dev/tty/something for Linux)

# Set motor mode to closed loop
motor_mode = 3
controller.send_command(cmds.MOTOR_MODE, motor_mode)

# Limit max velocity and acceleration
accel = 5
decel = 5
max_v = 5
controller.set_kinematics_params(accel, decel, max_v)



print(f"\nNew closed-loop max acceleration: {accel}")
print(f"New closed-loop max deceleration: {decel}")
print(f"New closed-loop max velocity: {max_v} \n")

Xarray = []
Yarray = []
timearray = []
theta = np.arange(0,2*np.pi,0.01)

for i in theta:
    Xarray.append(0.1*np.cos(i))
    Yarray.append(0.1*np.sin(i))

abscntr_1  = (controller.read_value(cmds.READ_ABSCNTR, 1))      # Read encoder counter absolute
abscntr_2  = (controller.read_value(cmds.READ_ABSCNTR, 2))      # Read encoder counter absolute
print(f"\nEncoder counts: \nENC1: {abscntr_1} \nENC2: {abscntr_2} \n\n")
var1 = input("Proceed? (y/n):\n")

if(var1 == "N"):
    exit()

print("Moving to origin...\n")
cmd = f"!P 1 {0} _!P 2 {0} "
result = controller.request_handler(cmd)
var2 = input("Is the origin in the correct position? (y/n):\n")


if(var2 == "y"):

    for i in range(0,len(Xarray)):
        t1 = time.time()
        time.sleep(1)

        (x, y) = (float(Xarray[i]), float(Yarray[i]))
        (enc1, enc2) = controller.convert_worldspace_to_encoder_cts(x, y)
        (enc1, enc2) = (round(enc1), round(enc2))
        print("Encoder Counts Sent: "+str(enc1)+", "+ str(enc2))
        cmd = f"!P 1 {enc1} _!P 2 {enc2} "
        result = controller.request_handler(cmd)
        t2 = time.time()
        timearray.append(t2-t1)
        
else:
    print("Recalibrate Robot")

plt.plot(Xarray,Yarray)
plt.show()