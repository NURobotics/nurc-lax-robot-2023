#from PyRoboteq import RoboteqHandler
from motor_controller import Controller
from PyRoboteq import roboteq_commands as cmds
import keyboard
import time

DRIVE_SPEED = 100
DWELL = 0.5 #time between commands
MAGIC_SCALAR = 1.73 #to adjust conversion from encoder counts to real-world posn
has_quit = False
estop_active = False #TODO: this may not necessarily be the case on startup; use FM to check status

abscntr_1 = None
abscntr_2 = None
motor_mode = 0

menu_text = \
	'ROBOTEQ MOTOR DRIVER INTERFACE \n' + \
	'WASD keys: move up/down/left/right \n' + \
	'e: read encoder counts \t\tf: read world coords  \t\th: set current posn as home \n' + \
	'u: set closed/open loop state \ti: get closed/open loop state  \tz: go to zero position \n' + \
	'r: go to encoder counts \tt: go to real-world posn \n' + \
	'q: quit client \t\t\tc: ESTOP \t\t\tx: RELEASE ESTOP'

modes_dict_text = {
	0: "Open Loop Speed Control",
	1: "Closed Loop Speed Control",
	2: "Closed Loop Position Relative Control", #-1000 to 1000 scale
	3: "Closed Loop Count Position (*)", #preferred. position input
	4: "Closed Loop Position Tracking (!)", #-1000 to 1000 scale. danger - setting mode to this caused rapid motion on startup
	5: "Torque Mode (!)", #don't use this for our project - can burn out a motor
	6: "Closed Loop Speed Position Control", #not preferred. speed input
}

def menu():
	print(menu_text)
	if estop_active:
		print("Estop is active")

controller = Controller(debug_mode = False, exit_on_interrupt = False)  # Create the controller object
is_connected = controller.connect("COM4") # connect to the controller (COM9 for windows, /dev/tty/something for Linux)

if (not is_connected):
    raise Exception("Error in connection")

#--------------------------#
controller.send_command(cmds.MOTOR_MODE, motor_mode)

# menu loop
menu()
while not has_quit:

	#ser.flush()
	#Menuing: use keyboard.is_pressed() to detect instant input

	if keyboard.is_pressed('w'):

		#send commands to move up
		while keyboard.is_pressed('w'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, -DRIVE_SPEED, -DRIVE_SPEED)

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)   

	###

	elif keyboard.is_pressed('s'):

		#send commands to move down
		while keyboard.is_pressed('s'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, DRIVE_SPEED, DRIVE_SPEED)

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)  

	###

	elif keyboard.is_pressed('a'):

		#send commands to move left
		while keyboard.is_pressed('a'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, -DRIVE_SPEED, DRIVE_SPEED)

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)  

	###

	elif keyboard.is_pressed('d'):

		#send commands to move right
		while keyboard.is_pressed('d'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, DRIVE_SPEED, -DRIVE_SPEED)

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)  

	###

	elif keyboard.is_pressed('q'):

		print('\nExiting client\n\n')
		has_quit = True # exit client
		# be sure to close the port
		#ser.close() 

	###

	elif keyboard.is_pressed('c'):

		print('\nHitting emergency stop \n\n')
		controller.send_command(cmds.EM_STOP) # this will send 0 argument command for emergency stop
		estop_active = True
		#has_quit = True; # exit client
		time.sleep(DWELL)
		menu()

	elif keyboard.is_pressed('x'):

		print('\nReleasing emergency stop \n\n')
		controller.send_command(cmds.REL_EM_STOP)
		estop_active = False

		time.sleep(DWELL)
		menu()

	###

	elif keyboard.is_pressed('e'):

		abscntr_1      = (controller.read_value(cmds.READ_ABSCNTR, 1))      # Read encoder counter absolute
		abscntr_2      = (controller.read_value(cmds.READ_ABSCNTR, 2))      # Read encoder counter absolute
		#abscntr_1 = int(abscntr_1.split('=')[-1])
		#abscntr_2 = int(abscntr_2.split('=')[-1])

		print(f"\nEncoder counts: \nENC1: {abscntr_1} \nENC2: {abscntr_2} \n\n")
		time.sleep(DWELL)
		menu()

	###

	elif keyboard.is_pressed('f'):

		abscntr_1      = (controller.read_value(cmds.READ_ABSCNTR, 1))      # Read encoder counter absolute
		abscntr_2      = (controller.read_value(cmds.READ_ABSCNTR, 2))      # Read encoder counter absolute
		try:
			abscntr_1 = int(abscntr_1.split('=')[-1])
			abscntr_2 = int(abscntr_2.split('=')[-1])
		
			(x, y) = controller.convert_enc_counts_to_posn(abscntr_1, abscntr_2)
			(x, y) = (round(MAGIC_SCALAR * x,3), round(MAGIC_SCALAR * y,3))
			print(f"\nWorld coords: ({x}m, {y}m) \n\n")
		except:
			print(f"Could not convert counts to int: \n{abscntr_1} \n{abscntr_2}")

		time.sleep(DWELL)
		menu()


	###

	elif keyboard.is_pressed('h'):
		
		print("\nSetting current position as home position: \n\n")

		#TODO: Check mode, see if it's closed-loop. Change mode to open-loop,
			#set the posn, and if putting it back into closed-loop mode,
			#clear out the previous commanded position so we don't shoot back there

		controller.send_command(cmds.SET_ENC_COUNTER, 1, 0) #first motor; set to zero
		controller.send_command(cmds.SET_ENC_COUNTER, 2, 0) #first motor; set to zero

		time.sleep(DWELL)
		menu()


	elif keyboard.is_pressed('z'):

		if motor_mode == 0:
			print("\nRoboteq is in open-loop mode; will not execute.\n\n")
		else:
			print("\nGoing to position (0,0):\n\n")
			controller.send_command(cmds.MOT_POS, 1, 0) #first motor; set to zero
			controller.send_command(cmds.MOT_POS, 2, 0) #first motor; set to zero

		time.sleep(DWELL)
		menu()

	elif keyboard.is_pressed('u'):
		#setter
		#controller.ser.flush() - this didn't work for clearing past inputs
		time.sleep(0.2)

		while True:
			print("\nValid operating modes:")
			for x in modes_dict_text.keys():
				print(f"{x}: {modes_dict_text[x]}")

			mode_temp = input("\nEnter a motor operating mode (0-6): ")

			#Restrict the user's string input to 0, 1, 2, 3, 4, or 6.
			if (mode_temp.isdigit() and int(mode_temp) < 7 and int(mode_temp) >= 0):
					if (int(mode_temp) == 5 or int(mode_temp) == 4):
						print("\nModes 4 and 5 are restricted for this project; select another.")
					else:
						print(f"Setting mode to: {modes_dict_text[int(mode_temp)]}\n\n")
						motor_mode = int(mode_temp)
						controller.send_command(cmds.MOTOR_MODE, motor_mode)
						break						

		time.sleep(DWELL)
		menu()

	elif keyboard.is_pressed('i'):
		#getter
		#no command found for this in the Roboteq manual. instead I'm keeping track of it manually
		#print(f"\nOperating mode: {modes_dict_text[motor_mode]} \n\n")
		op_mode1_raw = controller.read_value(cmds.MMODE_READ, 1)
		op_mode2_raw = controller.read_value(cmds.MMODE_READ, 2)
		print(f"\nOperating modes: \nM1: {op_mode1_raw} \nM2: {op_mode2_raw} \n\n")

		time.sleep(DWELL)
		menu()

	elif keyboard.is_pressed('r'):
		#go to encoder counts

		while True:
			print("\nEnter encoder count positions to travel to.")
			enc1_raw = input("ENC1: ")
			enc2_raw = input("ENC2: ")

			if (enc1_raw.isdigit() and enc2_raw.isdigit()):
				(enc1, enc2) = (int(enc1_raw), int(enc2_raw))
				print("\nSetting encoder counts.\n\n")
				controller.send_command(cmds.MOT_POS, 1, enc1)
				controller.send_command(cmds.MOT_POS, 2, enc2)
				break

			else:
				print("\nInvalid input; both numbers must be signed ints.")

		time.sleep(DWELL)
		menu()

	elif keyboard.is_pressed('t'):
		#go to real-world posn
		pass

#     drive_speed = 0
#     #print("Press S to stop")
#     #print("Press D to drive")

#     track_mode = False
#     while connected:

#         user_in = input("\nEnter a key to send a command: ")

#         if user_in == 'q':
#             print("Q pressed")
#             print("Stopping motion")
#             drive_speed = 0
#             controller.send_command(cmds.DUAL_DRIVE, drive_speed, drive_speed)
            
#         if user_in == 'x':
#             print("X pressed")
#             print("Starting to drive")
#             drive_speed = 250
#             controller.send_command(cmds.DUAL_DRIVE, drive_speed, drive_speed)


#         if user_in == 'e':
#             #read encoder count
#             abscntr_1      = controller.read_value(cmds.READ_ABSCNTR, 1)      # Read encoder counter absolute
#             abscntr_2      = controller.read_value(cmds.READ_ABSCNTR, 2)      # Read encoder counter absolute

#             print(f"Encoder counts: \nENC1: {abscntr_1} \nENC2: {abscntr_2}")

#         if user_in == 'p':
#             print("P pressed")
#             kp = input("Enter a new value for Kp: ")
#             controller.send_command(cmds.KP, kp)

#         if user_in == 'i':
#             print("I pressed")
#             ki = input("Enter a new value for Ki: ")
#             controller.send_command(cmds.KI, ki)

#         if user_in == 'd':
#             print("D pressed")
#             kd = input("Enter a new value for Kd: ")
#             controller.send_command(cmds.KD, kd)

#         if user_in == 'm':
#             print("M pressed")
#             track_mode = True

#             #get position before changes are applied
#             abscntr      = controller.read_value(cmds.READ_ABSCNTR, 1)      # Read encoder counter absolute
#             print(f"Encoder count: {abscntr}")
            
#             #NOTE! In the Roborun+ utility, make sure the Roboteq is currently
#             #in "closed loop count position" mode. Other closed loop position modes
#             #may work, but this is the tested method as of right now. 
#             desired_ct1 = input("Enter desired encoder count for Mot1 (will travel to this): ")
#             desired_ct2 = input("Enter desired encoder count for Mot2 (will travel to this): ")

#             controller.send_command(cmds.MOT_POS, 1, desired_ct1) # check how this command is supposed to wokr
#             controller.send_command(cmds.MOT_POS, 2, desired_ct2) # check how this command is supposed to wokr

#             '''
#             MOT_POS = "!P" # Go to motor absolute desired position
#             MPOS_REL = "!PR" # Go to relative desired position
#             NXT_POSR = "!PRX" # NEXT go to relative desired position
#             NXT_POS = "PX" # NEXT go to absolute desired position
#             '''

#         #don't use in this way - this code tries to do position tracking

#         #if user_in == 'r':
#         #    #reset encoder count to zero
#         #    abscntr      = controller.read_value(cmds.READ_ABSCNTR, 1)      # Read encoder counter absolute
#         #    print(f"Previous encoder count: {abscntr}")
#         #    controller.send_command(cmds.SET_ENC_COUNTER, 1, 0) #first motor; set to zero
#         #    abscntr      = controller.read_value(cmds.READ_ABSCNTR, 1)      # Read encoder counter absolute
#         #    print(f"New  encoder count: {abscntr}")
#         #    input("Press any key to continue.")


#         #check if there's a way to display which motor modes are currently active - 
#         #want to see if open loop or closed loop
        



#         #controller.send_command(cmds.DUAL_DRIVE, drive_speed, drive_speed)
#         #battery_amps = controller.read_value(cmds.READ_BATTERY_AMPS, 1) # Read value 1 of battery amps
#         #abscntr      = controller.read_value(cmds.READ_ABSCNTR, 1)      # Read encoder counter absolute

#         #print(f"Battery amps: {battery_amps}")
#         #print(f"Encoder count: {abscntr}") #extra thing added by Sean
            
            

        
        

