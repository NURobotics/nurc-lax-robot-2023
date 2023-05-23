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

def plot_field_point(x, y):
    """
    Plots a point with the given (x,y) coordinate on a plot.
    Any additional points passed to the function are plotted in a different color.
    """
    plt.rcParams["figure.figsize"] = [7.0, 3.5]   # default size from copied code, manipulate for iphone14 later
    plt.rcParams["figure.autolayout"] = True
    im = read_img("../media/lax_field.png")

    fig, ax = plt.subplots()
    ax.xaxis.set_tick_params(labelbottom=False)
    ax.yaxis.set_tick_params(labelleft=False)
    ax.set_xticks([])
    ax.set_yticks([])
    im = ax.imshow(im, extent=[-14, 14, -15, 4.5])   # units are meters, where to define 0 from?
    
    x_field_points.append(x)
    y_field_points.append(y)

    # Generating a random number in between 0 and 2^24
    color = random.randrange(0, 2**24)
    # Converting that number from base-10 (decimal) to base-16 (hexadecimal)
    hex_color = hex(color)
    # Converting hex (0x000000) to useable structure (#000000)
    std_color = "#" + hex_color[2:]
    colors.append(std_color)

    for i in range(len(x_field_points)):
        plt.plot(x_field_points[i], y_field_points[i], marker="o", markersize=13, markeredgewidth=1.5, markeredgecolor="black", markerfacecolor=colors[i], linestyle="None")
    plt.show()
    save_figure(fig, '../WebPages/field_plot.png')
    plt.pause(2)
    plt.close()


def plot_goal_point(x, y):
    """
    Plots a point with the given (x,y) coordinate on a plot.
    Any additional points passed to the function are plotted in a different color.
    """
    plt.rcParams["figure.figsize"] = [7.00, 3.50]   # default size from copied code, manipulate for iphone14 later
    plt.rcParams["figure.autolayout"] = True
    im = read_img("../media/lax_net_zones.png")
    fig, ax = plt.subplots()
    ax.xaxis.set_tick_params(labelbottom=False)
    ax.yaxis.set_tick_params(labelleft=False)
    ax.set_xticks([])
    ax.set_yticks([])
    m = ax.imshow(im, extent=[-1.719, 1.719, -1.250, 1.250])   # units are meters
    
    x_goal_points.append(x)
    y_goal_points.append(y)

    for i in range(len(x_goal_points)):
        plt.plot(x_goal_points[i], y_goal_points[i], marker="o", markersize=13, markeredgewidth=1.5, markeredgecolor="black", markerfacecolor=colors[i], linestyle="None")
    plt.show()
    save_figure(fig, '../WebPages/goal_plot.png')
    plt.pause(2)
    plt.close()


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
