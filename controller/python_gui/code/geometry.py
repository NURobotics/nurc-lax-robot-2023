import numpy as np
import sympy as sym
import dill
import time
from tqdm import tqdm

from helpers import *

#define frames and symbols. let L1 = L2, m1 = m2 for computational efficiency
#as this condition is unlikely to change

#--------symbolic transformation matrices, right side---------------#

#Rab = sym.Matrix([
#    [sym.cos(theta2), -sym.sin(theta2), 0],
#    [sym.sin(theta2),  sym.cos(theta2), 0],
#    [              0,                0, 1],
#])

#p_bd = sym.Matrix([0, -L, 0])

#Gab = SOnAndRnToSEn(Rab, [0, 0, 0])
#Gbd = SOnAndRnToSEn(sym.eye(3), p_bd)
#GdB2 = SOnAndRnToSEn(RdB2, [0, 0, 0])

#Gsa = SOnAndRnToSEn(sym.eye(3), [x, y, 0])
#Gsb = Gsa @ Gab
#Gsd = Gsb @ Gbd
#GsB2 = Gsd @ GdB2 #formerly Gsf


#------------line + box geometry; plotting geometry-------------------#

#Lnum and wnum defined under subs_dict

win_height = 600
win_width = 800
pixels_to_unit = 250 #2m occupies 500px

coordsys_len = 50
width  = win_width  / pixels_to_unit
height = win_height / pixels_to_unit

#let frame GUI be the coordinates as seen on the GUI,
#frame r be the frame at GUI coords (0,0) with axes in same direction
#as frame s. This is not in SE(3) so InvSEn() cannot be used with this.
GrGUI = np.array([
    [width/win_width,    0, 0, 0],
    [0, -height/win_height, 0, 0],
    [0,                  0, 1, 0],
    [0,                  0, 0, 1]
]) 

#GrGUI = np.array([
#    [x_scale,  0, 0, 0],
#    [0, -y_scale, 0, 0],
#    [0,        0, 1, 0],
#    [0,        0, 0, 1]
#]) 

Grs = SOnAndRnToSEn(np.identity(3), [width/2, -height/2, 0])
GsGUI = np.dot(InvSEn(Grs), GrGUI)


