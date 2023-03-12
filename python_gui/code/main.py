import sympy as sym
import numpy as np
import pandas as pd

import time
from tqdm import tqdm
import tkinter as tk

from GUI import GUI
from geometry import *
from helpers import *
from plotting_helpers import *

#-----------------tuning parameters-----------------------------#

#time parameters
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

#--------------canvas display--------------------#

gui.canvas.bind("<Motion>",           gui.on_mouse_over)
gui.canvas.bind("<Button>",           gui.on_click)
gui.root.protocol('WM_DELETE_WINDOW', gui.close) #forces closing of all Tk() functions
gui.canvas.pack()

gui.timer_id = gui.root.after(gui.framerate_ms, gui.on_frame)
gui.root.mainloop()

