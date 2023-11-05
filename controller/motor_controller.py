
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
        self.pulley_rad = 0.012 #mm; doesn't take into account belt thickness
        self.encoder_cpr = 1250
        self.MAGIC_SCALAR = 1.73 #to adjust conversion from encoder counts to real-world posn

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

    def convert_worldspace_to_encoder_cts(self, delta_x, delta_y):
        '''Documentation
        '''
        delta_x, delta_y = delta_x / self.MAGIC_SCALAR, delta_y / self.MAGIC_SCALAR

        #use corexy principles to find change in motor linear positions.
        #will need to adjust what "m1" and "m2" are defined as later
        delta_m1_lin =  delta_x - delta_y
        delta_m2_lin = -delta_x - delta_y

        #use x = r*theta to find angular change in motor
        delta_m1 = delta_m1_lin / self.pulley_rad
        delta_m2 = delta_m2_lin / self.pulley_rad
        encoder_cts_1 = delta_m1 * self.encoder_cpr
        encoder_cts_2 = delta_m2 * self.encoder_cpr

        return (encoder_cts_1, encoder_cts_2)


    def convert_enc_counts_to_posn(self, enc_count1, enc_count2):
        '''Takes counts of the encoders, and converts them into positions in x 
        and y in the real world. Uses the inverse of the coreXY transform.

        Returns: (x, y) - positions in real world
        '''

        dtheta_1 = enc_count1 / self.encoder_cpr
        dtheta_2 = enc_count2 / self.encoder_cpr

        dM1 = self.pulley_rad * dtheta_1
        dM2 = self.pulley_rad * dtheta_2

        dx = -0.5*(dM2 - dM1)
        dy = -0.5*(dM1 + dM2)
        dx, dy = self.MAGIC_SCALAR * dx, self.MAGIC_SCALAR * dy

        #assume initial position is at 0, so dx = x and dy = y
        return (dx, dy)
        
    def set_pid_params(self, kp, kd, ki):
        '''Sets gains for PID control all at once.'''
        self.send_command(cmds.KP, kp, 1)
        self.send_command(cmds.KD, kd, 1)
        self.send_command(cmds.KI, ki, 1)

        self.send_command(cmds.KP, kp, 2)
        self.send_command(cmds.KD, kd, 2)
        self.send_command(cmds.KI, ki, 2)

    def set_kinematics_params(self, accel, decel, max_v):
        #accel, decel, max velocity, rpms at max speed
        self.send_command(cmds.CL_MAX_ACCEL, accel, 1)
        self.send_command(cmds.CL_MAX_DECEL, decel, 1)
        self.send_command(cmds.CL_MAX_VEL, max_v, 1)

        self.send_command(cmds.CL_MAX_ACCEL, accel, 2)
        self.send_command(cmds.CL_MAX_DECEL, decel, 2)
        self.send_command(cmds.CL_MAX_VEL, max_v, 2)

    def read_PID(self):

        self.read_value(cmds.READ_KP, 1)
        self.read_value(cmds.READ_KI, 1)
        self.read_value(cmds.READ_KD, 1)

        self.read_value(cmds.READ_KP, 2)
        self.read_value(cmds.READ_KI, 2)
        self.read_value(cmds.READ_KD, 2)

    #init_coords = (0,0) #change based on actual posns read by encoders
    #deltax, deltay = [coord[i] - init_coords[i] for i in range(len(coord))]
    
    ##use corexy principles to find change in motor linear positions.
    ##will need to adjust what "m1" and "m2" are defined as later
    #delta_m1_lin = delta_y + delta_x
    #delta_m2_lin = delta_y - delta_x

    ##use x = r*theta to find angular change in motor
    #delta_m1 = delta_m1_lin / pulley_rad
    #delta_m2 = delta_m2_lin / pulley_rad

    #return (delta_m1, delta_m2)

#def gen_array_speed_cmds():
#    #check if position can be controlled by roboteq before doing this
#    pass
