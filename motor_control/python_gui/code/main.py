from GUI import GUI, init_gui
from geometry import win_height, win_width

if __name__ == "__main__":
    gui = GUI(win_height, win_width, "../media/lax_goalie_diagram.png", None) #namespace for variables: geometry.py
    init_gui(gui)

