#helper functions for GUI operations
import tkinter as tk
import time
import numpy as np
from PIL import Image, ImageTk
import os

from helpers import *
from geometry import *

def make_oval(canvas: tk.Canvas, center: tuple, width: int, height: int, fill: str='hotpink'):
    #from CS110; credit to Sarah Van Wart
    top_left = (center[0] - width, center[1] - height)
    bottom_right = (center[0] + width, center[1] + height)
    return canvas.create_oval([top_left, bottom_right], fill=fill, width=0) #return content ID

def make_circle(canvas: tk.Canvas, center: tuple, radius: int, fill: str='hotpink'):
    return make_oval(canvas, center, radius, radius, fill=fill) #return content ID

def make_grid_label(canvas, x, y, w, h, offset, pixels_to_unit):
    #from CS110; credit to Sarah Van Wart

    #apply offset by finding origin and applying conversion
    #from pixels to units in world
    width_world = w//pixels_to_unit
    height_world = h//pixels_to_unit
    
    origin_x = width_world//2
    origin_y = height_world//2
        
    xlabel, ylabel = (x/pixels_to_unit - origin_x, (h-y)/pixels_to_unit - origin_y - 0.5)

    #decide whether label is for x or y
    coord = xlabel if not xlabel == -origin_x else ylabel
    
    canvas.create_oval(
        x - offset, 
        y - offset, 
        x + offset,  
        y + offset, 
        fill='black'
    )
    canvas.create_text(
        x + offset, 
        y + offset, 
        text=str(round(coord,1)),
        anchor="sw", 
        font=("Purisa", 12)
    )

def make_grid(canvas, w, h, interval):
    #from CS110; credit to Sarah Van Wart
    #interval = the # of pixels per unit distance in the simulation
    
    # Delete old grid if it exists:
    canvas.delete('grid_line')
    offset = 2

    # Creates all vertical lines every 0.5 unit
    #for i in range(0, w, interval):
    for i in np.linspace(0, w, 2*w//interval+1).tolist()[:-1]:
        canvas.create_line(i, 0, i, h, tag='grid_line', fill='gray', dash=(2,2))
        make_grid_label(canvas, i, h, w, h, offset, interval)

    # Creates all horizontal lines every 0.5 unit
    #for i in range(0, h, interval):
    for i in np.linspace(0, h, 2*h//interval+1).tolist()[:-1]:
        canvas.create_line(0, i, w, i, tag='grid_line', fill='gray', dash=(2,2))
        make_grid_label(canvas, 0, i, w, h, offset, interval)
        
def make_coordsys(canvas, x, y, line_length, tag):
    #original work
    canvas.create_line(x, y, x + line_length,               y, arrow=tk.LAST, tag=tag+'x')
    canvas.create_line(x, y,               x, y - line_length, arrow=tk.LAST, tag=tag+'y')

def label_vertices(canvas, box1_vert_gui, box2_vert_gui):
    '''For debug purposes, put labels on each vertex of the boxes so we can see
    which impact conditions are occurring at a given point in time.

    Box1_vert_gui and box2_vert_gui are 10x0 flattened arrays, (x1, y1, x2, y2,...)
    '''
    #uses code from CS110's make_grid() function

    #remove 5th set of box vertices, as it closes the box structure
    box1_vert_gui = np.array(box1_vert_gui)[:-2]
    box2_vert_gui = np.array(box2_vert_gui)[:-2]

    canvas.delete("Vertices")
    offset = 2

    for i in range(len(box1_vert_gui)//2):
        x, y = box1_vert_gui[2*i : 2*i + 2]
        canvas.create_text(
            x + offset, 
            y - offset, 
            text=f"V1{i+1}",
            anchor="s", 
            font=("Purisa", 8),
            tag="Vertices"
        )

    for i in range(len(box2_vert_gui)//2):
        x, y = box2_vert_gui[2*i : 2*i + 2]
        canvas.create_text(
            x + offset, 
            y - offset, 
            text=f"V2{i+1}",
            anchor="s", 
            font=("Purisa", 8),
            tag="Vertices"
        )

def make_invisible(canvas,id):
    #my own original work from CS110
    canvas.itemconfigure(id, state='hidden')

def make_visible(canvas,id):
    #my own original work from CS110
    canvas.itemconfigure(id, state='normal')

def draw_image(canvas:tk.Canvas, gui, center:tuple, file_path:str, size:int=0,
                  scale:tuple=(1,1), tags:str=None,state='normal'):
    '''
    Makes an image onto the TKinter canvas. Uses a file located at file_path
    relative to the current code.

    Args:
        canvas(TK): the TKinter canvas for displaying images
        gui (TK root/master): necessary for stability when importing 'helpers' into 'main'
        center(Tuple): the location of the center of the image
        file_path(Str): the path of the .PNG you want to paste onto the Tkinter
                canvas. can include folder as well
        size(Int) - optional: the size you want to assign to the image. if size="0", as
                set by default, the image won't be resized from default
        tags(Str) - optional: the identifying word to use in order to group
                and move around an image of a certain type
        state(Str) - optional: used to turn a tagged image from visible
                (the 'normal' state) to invisible (state='hidden')

    Returns:
        the ID for the image; position and visibility can be modified
    '''
    #my own work from CS110

    # adds folder directory to path
    directory = os.path.dirname(os.path.realpath(__file__))       
    file_path = os.path.join(directory, file_path)
    image = Image.open(file_path)

    # finds default width and height of png

    default_height = image.size[1]
    default_width = image.size[0]

    # changes height of image if needed. an input of '0' will tell the
    # program that the user wants to use the default height.

    if size != 0:
        # "size" input will become the new height       
        size_ratio = size/default_height
        height = size
        width = int(round(default_width * size_ratio))

        # antialiasing necessary to keep edges of image smooth when scaling
        image = image.resize((width,height), Image.ANTIALIAS)
    
    if scale != (1,1):
        print("Rescaling...")
        image = image.resize((int(default_width * scale[0]), \
                             int(default_height * scale[1])), Image.ANTIALIAS)
    else:
        print("Not rescaling lol")


    # turns the file name into a tkinter Photo Image using PIL
    photo_image = ImageTk.PhotoImage(image)
    
    # to keep the image on the screen
    label = tk.Label(gui, image=photo_image)
    label.image = photo_image

    ID = canvas.create_image(center, image = photo_image, tags=tags,state=state)
    return ID






