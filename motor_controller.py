
from PyRoboteq import roboteq_handler
from PyRoboteq import roboteq_commands as cmds


def convert_worldspace_to_motor_rot(coord):
    '''Takes a position in the real world, and converts it to necessary
    angles of rotation of the two motors in the corexy setup.
    https://corexy.com/theory.html

    Returns: (delta_m1, delta_m2) - rotations of each motor
    '''
    pulley_rad = 0 #update with actual pulley rad
    init_coords = (0,0) #change based on actual posns read by encoders
    deltax, deltay = [coord[i] - init_coords[i] for i in range(len(coord))]
    
    #use corexy principles to find change in motor linear positions.
    #will need to adjust what "m1" and "m2" are defined as later
    delta_m1_lin = delta_y + delta_x
    delta_m2_lin = delta_y - delta_x

    #use x = r*theta to find angular change in motor
    delta_m1 = delta_m1_lin / pulley_rad
    delta_m2 = delta_m2_lin / pulley_rad

    return (delta_m1, delta_m2)

def read_motor_controller_vals():
    #consider making a struct that contains all the important params, and updating every n cycles
    #by reading from motor controller
    pass

    '''
    Motor commands of interest:
    READ_MOTOR_AMPS = "?A" # Read current motor amperage
    READ_BATTERY_AMPS = "?BA" # Read battery amps
    READ_BL_MOTOR_RPM = "?BS" # Read brushless motor speed in RPM
    READ_BLRSPEED = "?BSR" # Read brushless motor speed as 1/100 of max RPM
    READ_ABSCNTR = "?C" # Read encoder counter absolute
    READ_BLCNTR = "?CB" # Read absolute brushless counter
    READ_PEAK_AMPS = "?DPA" # Read DC/Peak Amps
    READ_DREACHED = "?DR" # Read destination reached
    READ_FLTFLAG = "?FF" # Read fault flags
    READ_MOTCMD = "?M" # Read motor command applied
    READ_TEMP = "?T" # Read controller temperature
    READ_VOLTS = "?V" # Read voltage measured
    '''

def gen_array_speed_cmds():
    #check if position can be controller by roboteq before doing this
    pass

def set_pid_params():
    pass

def set_kinematics_params():
    #accel, decel, max velocity, rpms at max speed
    pass