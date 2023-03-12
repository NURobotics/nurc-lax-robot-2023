import tkinter as tk
import numpy as np

from geometry import *
from helpers import *
from plotting_helpers import *

###########

class GUI:

    def __init__(self, win_height, win_width, photo_filepath):

        #future improvement: should inherit from the Tk class
        self.root = tk.Tk()
        self.root.title("Lacrosse Goalie Simulation")
        self.canvas = tk.Canvas(self.root, bg="white", height=win_height, width=win_width)
        self.win_height = win_height
        self.win_width = win_width
        self.photoID = draw_image(self.canvas, self.root, \
            (self.win_width//2, self.win_height//2), photo_filepath, size=0,
                                  #scale = (1,1/0.85), 
                                  tags='background')#, state='hidden')

        #member data we expect to change on each loop
        self.timer_handle = None #set this from the outside once canvas is packed
        self.last_frametime = 0
        self.q_ind = 0
        self.impact_photoID = None
        self.mouse_posn_gui = [win_width//2, win_height//2]
        self.mouse_posn_s = [0,0]

    ###

    #these values are determined externally, but loading them all in __init__
    #would be too long, so do it here

    def load_arrays(self, line_coords_mat, vertices_mat):
        self.line_coords_mat = line_coords_mat
        self.vertices_mat    = vertices_mat

    def load_gui_params(self, L, w, coordsys_len, GsGUI, framerate, photo_filepath):
        self.L = L
        self.w = w
        self.coordsys_len = coordsys_len
        self.GsGUI = GsGUI
        self.framerate_ms = framerate

    #-----------------------------------#

    def get_GUI_coords(self, q):
        '''
        Takes the present value of the state array and returns the 
        coordinates of the key items on the GUI: the coords of
        the lines for the two strings, and the coords of the boxes
        for the two masses.
    
        Arguments:
        - q: current value of extended state array [q; qdot]
        - line_coords_mat: a 4xn array, n = 2 points per line,
            with the coordinates of lines in their reference frames
        - vertices_mat: a 4x5 array (4 vertices per box, plus the initial
            coordinate repeated) with coordinates of vertices of the boxes
            in their reference frames
        - GsGUI: transformation of points from space frame to GUI frame
            (note: not SE(3) - scaling + mirroring operations)
        - L: length of string
        - w: width of box
    
        Returns:   
        - box1_vert_gui:    cods of object in GUI frame 
        - box2_vert_gui:    coords of object in GUI frame 
        - line1_coords_gui: coords of object in GUI frame 
        - line2_coords_gui: coords of object in GUI frame
        '''
    
        ##extract coords
        #x, y, theta1, theta2, phi1, phi2 = q[0:6]
        
        ##define frames

        ##---------------right side---------------#

        #Rab = np.array([
        #    [np.cos(theta2), -np.sin(theta2), 0],
        #    [np.sin(theta2),  np.cos(theta2), 0],
        #    [              0,                0, 1],
        #])

        #RdB2 = np.array([
        #    [np.cos(phi2), -np.sin(phi2), 0],
        #    [np.sin(phi2),  np.cos(phi2), 0],
        #    [            0,              0, 1],
        #])

        #p_bd = np.array([0, -self.L, 0])

        #Gab = SOnAndRnToSEn(Rab, [0, 0, 0])
        #Gbd = SOnAndRnToSEn(np.eye(3), p_bd)
        #GdB2 = SOnAndRnToSEn(RdB2, [0, 0, 0])

        #Gsa = SOnAndRnToSEn(np.eye(3), [x, y, 0])
        #Gsb = Gsa @ Gab
        #Gsd = Gsb @ Gbd
        #GsB2 = Gsd @ GdB2 #formerly Gsf


        ##---------------left side---------------#

        #Rac = np.array([
        #    [np.cos(theta1), -np.sin(theta1), 0],
        #    [np.sin(theta1),  np.cos(theta1), 0],
        #    [             0,               0, 1],
        #])

        #ReB1 = np.array([
        #    [np.cos(phi1), -np.sin(phi1), 0],
        #    [np.sin(phi1),  np.cos(phi1), 0],
        #    [           0,             0, 1],
        #])

        #p_ce = np.array([0, -self.L, 0])

        #Gac = SOnAndRnToSEn(Rac, [0, 0, 0])
        #Gce = SOnAndRnToSEn(np.eye(3), p_ce)
        #GeB1 = SOnAndRnToSEn(ReB1, [0, 0, 0])

        #Gsa = SOnAndRnToSEn(np.eye(3), [x, y, 0])
        #Gsc = Gsa @ Gac
        #Gse = Gsc @ Gce
        #GsB1 = Gse @ GeB1 #formerly Gsg

        ##make objects in the frames of interest - home frame --> s frame
        #line1_coords_s  = np.dot(Gsc,  self.line_coords_mat)
        #line2_coords_s  = np.dot(Gsb,  self.line_coords_mat)
        #box1_vertices_s = np.dot(GsB1, self.vertices_mat)
        #box2_vertices_s = np.dot(GsB2, self.vertices_mat)

        #-----------#

        #convert object positions into the frame of the canvas
        #box1_vert_gui    = np.dot(np.linalg.inv(self.GsGUI), box1_vertices_s)[0:2, :] 
    
        #return box1_vert_gui, \
        #       box2_vert_gui, \
        #       line1_coords_gui, \
        #       line2_coords_gui
        return None, None, None, None

    #-----------------------------------#

    #event handlers

    def on_mouse_over(self, event):
        self.canvas.coords('user_posx', 
                     event.x, event.y,
                     event.x + self.coordsys_len, event.y)  
        self.canvas.coords('user_posy', 
                     event.x, event.y,
                     event.x, event.y - self.coordsys_len)
        self.mouse_posn_gui = [event.x, event.y]

        #calculate position of user in s frame
        mouse_posn_guibar = np.array([event.x, event.y, 0, 1])
        self.mouse_posn_s = np.dot(GsGUI, mouse_posn_guibar)[0:2]

    def close(self):
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass

   
    def on_frame(self):
        ''' Animation update event, passed to the Tkinter canvas. Uses real-time
        data being collected and processed using the dxdt() function and the impact
        handling functions.
        '''
    
        #compare current real time to previous
        elapsed = time.perf_counter() - self.last_frametime
        elapsed_ms = int(elapsed*1000)
        prev_impact = False
    
        #elapsed time is a fraction of the total framerate in ms
        frame_delay = self.framerate_ms - elapsed_ms

        #apply updates to object posns
        if self.q_ind == 0:
            #create objects on the canvas
            linewidth = 2

        else:
            #update positions of the objects by tags
            pass
    
        #see plotting_helpers.py
        #label_vertices(self.canvas, box1_vert_gui, box2_vert_gui)
        self.q_ind += 1
    
        #---------------------#
    
        #update the frame delay of the timer object
        self.timer_handle = self.root.after(frame_delay, self.on_frame)
    
        #update last_frametime for next frame
        self.last_frametime = time.perf_counter()

    def on_click(self, event):
        print(self.mouse_posn_s)
        #print([event.x, event.y])
        