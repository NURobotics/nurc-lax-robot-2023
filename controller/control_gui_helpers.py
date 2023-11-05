'''
Global variables and helper functions used in motor_control_gui.py.
'''

drive_speed = 100
DWELL = 0.5 #time between commands
has_quit = False
estop_active = False #TODO: this may not necessarily be the case on startup; use FM to check status

abscntr_1 = None
abscntr_2 = None
motor_mode = 0

menu_text = \
	'ROBOTEQ MOTOR DRIVER INTERFACE \n' + \
	'WASD keys: move up/down/left/right \n' + \
	'1234 keys: move diagonally, UR/DL/UL/DR \n\n' + \
	'e: read encoder counts \t\tf: read world coords  \t\th: set current posn as home \n' + \
	'u: set closed/open loop state \ti: get closed/open loop state  \tz: go to zero position \n' + \
	'r: go to encoder counts \tt: go to real-world posn \tk: send new Kp, Ki, Kd\n' + 'a: read PID parameters\n'+ \
	'm: get open-loop drive speed \tn: set open-loop drive speed \tl: game controller mode \n' + \
	'b: send raw serial cmds \tp: set max closed-loop speed and accel\n' + \
	'g: visual GUI (closed-loop position) \n' + \
	'q: quit client \t\t\tc: ESTOP \t\t\tx: RELEASE ESTOP'

#later: use j and k for setting kp, ki, kd for diff modes

modes_dict_text = {
	0: "Open Loop Speed Control",
	1: "Closed Loop Speed Control",
	2: "Closed Loop Position Relative Control", #-1000 to 1000 scale
	3: "Closed Loop Count Position (*)", #preferred. position input
	4: "Closed Loop Position Tracking (!)", #-1000 to 1000 scale. danger - setting mode to this caused rapid motion on startup
	5: "Torque Mode (!)", #don't use this for our project - can burn out a motor
	6: "Closed Loop Speed Position Control", #not preferred. speed input
}

#for open-loop speed control - WASD controls
drive_speeds_dict = {
	'w': ( -drive_speed, -drive_speed),
	's': ( drive_speed, drive_speed),
	'a': ( -drive_speed, drive_speed),
	'd': ( drive_speed, -drive_speed),
	'1': ( 0, -drive_speed),
	'2': ( 0, drive_speed),
	'3': ( -drive_speed, 0),
	'4': ( drive_speed, 0),
}


def menu():
	print(menu_text)
	if estop_active:
		print("Estop is active")


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False