from motor_controller import Controller
from PyRoboteq import roboteq_commands as cmds
from control_gui_helpers import *
#import keyboard
import time
import sys
import os

#for visual GUI
curr_dir = os.path.dirname(os.getcwd())
new_dir = curr_dir + '\\motor_control\\python_gui\\code'
sys.path.append(new_dir)

#------------------------------------------------#

controller = Controller(debug_mode = False, exit_on_interrupt = False)  # Create the controller object
is_connected = controller.connect("/dev/tty.usbmodemC13E847AFFFF1")

if (not is_connected):
	raise Exception("Error in connection")

#--------------------------#
# Set the motor mode to closed loop count position
motor_mode = 3
controller.send_command(cmds.MOTOR_MODE, 1, motor_mode)
controller.send_command(cmds.MOTOR_MODE, 2, motor_mode)

# Define the limits in real world coordinates in meters
goal_height = 1.92 # meters
goal_width = 2.75 # meters
end_effector_height = 0.331 # meters
end_effector_width = 0.466 # meters

# In the infinite control loop there needs to be software to protect the control signal from destroying the frame
commanded_position = [0,1]
# Commanded position center point is the top and 
if commanded_position >

