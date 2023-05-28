import matplotlib.pyplot as plt
import random
import time
import os

plt.ion()   #interactive mode

# initialize arrays
x_field_points = []
y_field_points = []
x_goal_points = []
y_goal_points = []
colors = []

def read_img(localpath):
    '''Reads an image from a place on our PC relative to the current script.
    '''
    return plt.imread(os.path.join(os.path.dirname(__file__), localpath))

def save_figure(figure, localpath):
    '''Saves a figure to a location relative to the current script.
    '''
    figure.savefig(os.path.join(os.path.dirname(__file__), localpath))

def plot_point(x,y, filepath_in, filepath_out, extent, x_points, y_points):
    '''The base code for plot_field_point() and plot_goal_point(). We'll then
    make those two functions a variant on this one.
    '''

    plt.rcParams["figure.figsize"] = [7.0, 3.5]   # default size from copied code, manipulate for iphone14 later
    plt.rcParams["figure.autolayout"] = True
    im = read_img(filepath_in)

    fig, ax = plt.subplots()
    ax.xaxis.set_tick_params(labelbottom=False)
    ax.yaxis.set_tick_params(labelleft=False)
    ax.set_xticks([])
    ax.set_yticks([])
    im = ax.imshow(im, extent=extent)   # units are meters, where to define 0 from?
    
    x_points.append(x)
    y_points.append(y)

    gen_color()

    for i in range(len(x_points)):
        plt.plot(x_points[i], y_points[i], \
                 marker="o", \
                 markersize=13, \
                 markeredgewidth=1.5, \
                 markeredgecolor="black", \
                 markerfacecolor=colors[i], \
                 linestyle="None" \
        )
    plt.show()
    save_figure(fig, filepath_out)
    plt.pause(2)
    plt.close()

def plot_field_point(x, y):
    '''Plots a point with the given (x,y) coordinate on a plot.
    Any additional points passed to the function are plotted in a different color.
    '''
    extent = [-14, 14, -15, 4.5]
    filepath_in = "../media/lax_field.png"
    filepath_out = '../WebPages/field_plot.png'
    x_points = x_field_points
    y_points = y_field_points
    plot_point(x,y, filepath_in, filepath_out, extent, x_points, y_points)

def plot_goal_point(x, y):
    '''  Plots a point with the given (x,y) coordinate on a plot.
    Any additional points passed to the function are plotted in a different color.
    '''
    extent = [-1.719, 1.719, -1.250, 1.250]
    filepath_in = "../media/lax_net_zones.png"
    filepath_out = '../WebPages/goal_plot.png'
    x_points = x_goal_points
    y_points = y_goal_points
    plot_point(x,y, filepath_in, filepath_out, extent, x_points, y_points)

def gen_color():
    '''Generates a random color in between 0 and 2^24, converts from base-10 to hex, and 
    formats it in #123456 format.
    '''
    color = random.randrange(0, 2**24) #generation
    hex_color = hex(color) #conversion
    std_color = "#" + hex_color[2:] #formatting
    colors.append(std_color)

if __name__ == '__main__':

    #test out the plotting
    plot_field_point(0, 0)  # plots (2,3) in blue
    plot_goal_point(0,0)
    plot_field_point(12, 0)
    plot_goal_point(1,0)
    plot_field_point(-12, 0)  # plots (4,5) in red
    plot_goal_point(-1.375,0)
    plot_field_point(0, -8)  # plots (6,1) in green
    plot_goal_point(0.344, 0.25)
    plot_field_point(0, -12)
    plot_goal_point(-0.25, -0.75)

