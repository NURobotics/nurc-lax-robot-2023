import numpy as np
from matplotlib import pyplot as plt
import random

plt.rcParams["figure.figsize"] = [7.00, 3.50]   # default size from copied code, manipulate for iphone14 later
plt.rcParams["figure.autolayout"] = True
im = plt.imread("/Users/emilygordon/NURC/media/cropped_lax_net.png") # this path likely needs to change for host computer
fig, ax = plt.subplots()
ax.xaxis.set_tick_params(labelbottom=False)
ax.yaxis.set_tick_params(labelleft=False)
ax.set_xticks([])
ax.set_yticks([])
im = ax.imshow(im, extent=[-1.375, 1.375, -1.000, 1.000])   # units are meters

# function, takes in datasets xpoints, ypoints to plot on image of goal
def goal_display(xpoints, ypoints):     # should the function accept arrays or tuples?
    xpoints = np.array(xpoints)
    ypoints = np.array(ypoints)

    for i in range(len(xpoints)):

        # Generating a random number in between 0 and 2^24
        color = random.randrange(0, 2**24)
        # Converting that number from base-10 (decimal) to base-16 (hexadecimal)
        hex_color = hex(color)
        # Converting hex (0x000000) to useable structure (#000000)
        std_color = "#" + hex_color[2:]
        plt.plot(xpoints[i], ypoints[i], marker="o", markersize=10, markeredgecolor="black", markerfacecolor=std_color, linestyle="None") # how big should the "ball" be?
        
    plt.show()

goal_display([0, 0.5, -0.5], [0, 0.5, -0.5])
fig.savefig('/Users/emilygordon/NURC/WebPages/goal_plot.png')