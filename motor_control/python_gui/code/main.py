import sympy as sym
import numpy as np
import pandas as pd

import time
from tqdm import tqdm
import tkinter as tk

import sys
import os

from GUI import GUI
from geometry import *
from helpers import *
from plotting_helpers import *

parent_dir = os.path.dirname(os.getcwd())
sys.path.append("C:/Users/seanp/Documents/lacrosse/code/nurc-lax-bot-2023/motor_control")

from PyRoboteq import roboteq_commands as cmds
from motor_controller import Controller

#----------------initialize GUI----------------------#

framerate_ms = 20
gui = GUI(win_height, win_width, "../media/lax_goalie_diagram.png") #namespace for variables: geometry.py
gui.load_gui_params(1, 1, coordsys_len, GsGUI, 
                    framerate_ms, '../sprites/impact_sparks.png') #plotting_helpers.py

#----------------populate canvas----------------------#

s_frame       = make_coordsys(gui.canvas, win_width/2, win_height/2, coordsys_len, tag='s_frame')
#make_grid(                    gui.canvas, win_width,   win_height,   pixels_to_unit)
user_coordsys = make_coordsys(gui.canvas, win_width/2, win_height/2, coordsys_len, tag='user_pos')
s_frame =       make_coordsys(gui.canvas, win_width/2, win_height/2, coordsys_len, tag='s_frame')

#----------------load motor controller----------------------#

drive_speed = 100
DWELL = 0.5 #time between commands
has_quit = False
estop_active = False #TODO: this may not necessarily be the case on startup; use FM to check status

abscntr_1 = None
abscntr_2 = None
motor_mode = 0

#later: use j and k for setting kp, ki, kd for diff modes

modes_dict_text = {
	0: "Open Loop Speed Control",
	1: "Closed Loop Speed Control",
	2: "Closed Loop Position Relative Control", #-1000 to 1000 scale
	3: "Closed Loop Count Position (*)", #preferred. position input
	4: "Closed Loop Position Tracking (!)", #-1000 to 1000 scale. danger - setting mode to this caused rapid motion on startup
	5: "Torque Mode (!)", #don't use this for our project - can burn out a motor
	6: "Closed Loop Speed Position Control", #not preferred. speed input
}

controller = Controller(debug_mode = False, exit_on_interrupt = False)  # Create the controller object
is_connected = controller.connect("COM4") # connect to the controller (COM9 for windows, /dev/tty/something for Linux)

if (not is_connected):
    raise Exception("Error in connection")

#--------------------------#
controller.send_command(cmds.MOTOR_MODE, motor_mode)



#--------------canvas display--------------------#

gui.canvas.bind("<Motion>",           gui.on_mouse_over)
gui.canvas.bind("<Button>",           gui.on_click)
gui.root.protocol('WM_DELETE_WINDOW', gui.close) #forces closing of all Tk() functions
gui.canvas.pack()

gui.timer_id = gui.root.after(gui.framerate_ms, gui.on_frame)
gui.root.mainloop()

