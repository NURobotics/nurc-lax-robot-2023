
from PyRoboteq.roboteq_handler import RoboteqHandler
from PyRoboteq import roboteq_commands as cmds

class Controller(RoboteqHandler):
    '''A simple structure to describe the motor controller at a higher level
    than the base capabilities of class RoboteqHandler.

    This class includes:
    - Member data describing current params being read from the Roboteq
    - Functions to handle PID control
    - Functions to convert from real-world space to motor space
    '''

    def __init__(self, exit_on_interrupt = False, debug_mode = False):
        super().__init__(exit_on_interrupt, debug_mode)

    def read_curr_state(self):
        '''Read all relevant values from the Roboteq at once. Depending on baud rate,
        this may be a time-consuming operation - check later to see if it needs to be 
        optimized.

        Structure of read_value:  command: str = "", parameter = "" (parameter is usually 1 for first value)

        Returns: none; edits member data
        '''
        self.motor_amps   = self.read_value(cmds.READ_MOTOR_AMPS,1)    # Read current motor amperage
        self.battery_amps = self.read_value(cmds.READ_BATTERY_AMPS,1)  # Read battery amps
        self.bl_motor_rpm = self.read_value(cmds.READ_BL_MOTOR_RPM, 1) # Read brushless motor speed in RPM
        self.blrspeed     = self.read_value(cmds.READ_BLRSPEED, 1)     # Read brushless motor speed as 1/100 of max RPM
        self.abscntr      = self.read_value(cmds.READ_ABSCNTR, 1)      # Read encoder counter absolute
        self.blcntr       = self.read_value(cmds.READ_BLCNTR, 1)       # Read absolute brushless counter
        self.peak_amps    = self.read_value(cmds.READ_PEAK_AMPS, 1)    # Read DC/Peak Amps
        self.dreached     = self.read_value(cmds.READ_DREACHED, 1)     # R4ead destination reached
        self.fltflag      = self.read_value(cmds.READ_FLTFLAG, 1)      # Read fault flags
        self.motcmd       = self.read_value(cmds.READ_MOTCMD, 1)       # Read motor command applied
        self.temp         = self.read_value(cmds.READ_TEMP, 1)         # Read controller temperature
        self.volts        = self.read_value(cmds.READ_VOLTS, 1)        # Read voltage measured

        
def set_pid_params():
    pass

def set_kinematics_params():
    #accel, decel, max velocity, rpms at max speed
    pass

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



#def gen_array_speed_cmds():
#    #check if position can be controlled by roboteq before doing this
#    pass
