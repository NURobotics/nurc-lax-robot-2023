#from PyRoboteq import RoboteqHandler
from motor_controller import Controller
from PyRoboteq import roboteq_commands as cmds
import keyboard
import time

#for PS controller
import hid

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
	'r: go to encoder counts \tt: go to real-world posn \n' + \
	'm: get open-loop drive speed \tn: set open-loop drive speed\n' + \
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
			controller.send_command(cmds.DUAL_DRIVE, -drive_speed, -drive_speed)

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)   

	###

	elif keyboard.is_pressed('s'):

		#send commands to move down
		while keyboard.is_pressed('s'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, drive_speed, drive_speed)

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)  

	###

	elif keyboard.is_pressed('a'):

		#send commands to move left
		while keyboard.is_pressed('a'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, -drive_speed, drive_speed)

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)  

	###

	elif keyboard.is_pressed('d'):

		#send commands to move right
		while keyboard.is_pressed('d'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, drive_speed, -drive_speed)

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)  

	###

	#diagonal motion commands

	if keyboard.is_pressed('1'):

		#send commands to move up-right
		while keyboard.is_pressed('1'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, 0, -drive_speed)
			pass

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)   

	###

	elif keyboard.is_pressed('2'):

		#send commands to move down-left
		while keyboard.is_pressed('2'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, 0, drive_speed)
			pass

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)  

	###

	elif keyboard.is_pressed('3'):

		#send commands to move up-left
		while keyboard.is_pressed('3'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, -drive_speed, 0)
			pass

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)  

	###

	elif keyboard.is_pressed('4'):

		#send commands to move down-right
		while keyboard.is_pressed('4'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, drive_speed, 0)
			pass

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)  



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
			(x, y) = (round(x,3), round(y,3))
			print(f"\nWorld coords: ({x}m, {y}m) \n\n")
		except:
			print(f"Could not convert counts to int: \n{abscntr_1} \n{abscntr_2}")

		time.sleep(DWELL)
		menu()


	###

	elif keyboard.is_pressed('h'):
		
		if motor_mode != 0:
			print("\nSet Roboteq to Open Loop Mode first; will not execute.\n\n")
		else:
			print("\nSetting current position as home position: \n\n")

			#TODO: Check mode, see if it's closed-loop. Change mode to open-loop,
				#set the posn, and if putting it back into closed-loop mode,
				#clear out the previous commanded position so we don't shoot back there
			
			controller.send_command(cmds.SET_ENC_COUNTER, 1, 0) #first motor; set to zero
			controller.send_command(cmds.SET_ENC_COUNTER, 2, 0) #first motor; set to zero

		time.sleep(DWELL)
		menu()


	elif keyboard.is_pressed('z'):

		if motor_mode != 3:
			print("\nSet Roboteq to Closed Loop Count Position first; will not execute.\n\n")
		else:
			print("\nGoing to position (0,0):\n\n")
			#controller.send_command(cmds.MOT_POS, 1, 0) #first motor; go to zero
			#controller.send_command(cmds.MOT_POS, 2, 0) #second motor; go to zero
			#controller.send_command(cmds.MOT_POS, 1, 0) #first motor; go to zero
			#time.sleep(0.05)
			#controller.send_command(cmds.MOT_POS, 1, 0) #second motor; go to zero
			#controller.send_command(cmds.NXT_POS, 2, 0) #second motor; go to zero
			#controller.send_command(cmds.NXT_POS, 1, 0) #first motor; go to zero

			#controller.send_command(cmds.NXT_POS, 1, 0) #second motor; go to zero

			controller.send_command(cmds.MOT_POS, 1, 0) #second motor; go to zero
			time.sleep(1)
			controller.send_command(cmds.MOT_POS, 2, 0) #second motor; go to zero



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
						controller.send_command(cmds.MOTOR_MODE, 1, motor_mode)
						controller.send_command(cmds.MOTOR_MODE, 2, motor_mode)
						break						

		time.sleep(DWELL)
		menu()

	elif keyboard.is_pressed('i'):
		#getter
		print("\nValid operating modes:")
		for x in modes_dict_text.keys():
			print(f"{x}: {modes_dict_text[x]}")

		op_mode1_raw = controller.read_value(cmds.MMODE_READ, 1)
		op_mode2_raw = controller.read_value(cmds.MMODE_READ, 2)
		print(f"\nOperating modes: \nM1: {op_mode1_raw} \nM2: {op_mode2_raw} \n\n")

		time.sleep(DWELL)
		menu()

	elif keyboard.is_pressed('r'):
		#go to encoder counts
		if motor_mode != 3:
			print("\nSet Roboteq to Closed Loop Count Position first; will not execute.\n\n")
		
		else:
			while True:
				print("\nEnter encoder count positions to travel to.")
				enc1_raw = input("ENC1: ")
				enc2_raw = input("ENC2: ")

				if (enc1_raw.isdigit() and enc2_raw.isdigit()):
					(enc1, enc2) = (int(enc1_raw), int(enc2_raw))
					print("\nSetting encoder counts.\n\n")
					controller.send_command(cmds.MOT_POS, 1, enc1)
					controller.send_command(cmds.MOT_POS, 2, enc2)
					#controller.send_command(cmds.MOT_POS, 1, enc1)
					#controller.send_command(cmds.NXT_POS, 2, enc2)
					break

				else:
					print("\nInvalid input; both numbers must be signed ints.")

		time.sleep(DWELL)
		menu()

	elif keyboard.is_pressed('t'):
		#go to real-world posn
		if motor_mode != 3:
			print("\nSet Roboteq to Closed Loop Count Position first; will not execute.\n\n")
			
		else:
			while True:
				print("\nEnter real world position (in meters) to travel to.")
				x_raw = input("x (m): ")
				y_raw = input("y (m): ")

				if (isfloat(x_raw) and isfloat(y_raw)):
					(x, y) = (float(x_raw), float(y_raw))
					(enc1, enc2) = controller.convert_worldspace_to_encoder_cts(x, y)
					(enc1, enc2) = (round(enc1), round(enc2))

					print(f"\nEncoder counts calculated to go to: \nENC1: {enc1} \nENC2: {enc2}")
					break

				else:
					print("\nInvalid input; both numbers must be floats.")

			decision = input("\nEnter 'y' to go to these encoder counts. ")
			if 'y'.__eq__(decision.lower()):
				print("\nSetting encoder counts.\n\n")
				controller.send_command(cmds.MOT_POS, 1, enc1)
				controller.send_command(cmds.MOT_POS, 2, enc2)
				#controller.send_command(cmds.MOT_POS, 1, enc1)
				#controller.send_command(cmds.NXT_POS, 2, enc2)

		time.sleep(DWELL)
		menu()

	elif keyboard.is_pressed('m'):
		#get motor speed
		print(f"\nMotor speed (0-1000): {drive_speed} \n\n")

		time.sleep(DWELL)
		menu()

	elif keyboard.is_pressed('n'):
		#set new motor speed
		while True:
			speed_raw = input("\nEnter new open-loop drive speed between 0 and 1000 (default: 100): ")

			if (speed_raw.isdigit() and int(speed_raw) > 0 and int(speed_raw) < 1000):

				drive_speed = int(speed_raw)
				print(f"\nNew drive speed: {drive_speed} \n\n")
				break

			else:
				print("\nInvalid input; enter an int between the specified bounds.")

		time.sleep(DWELL)
		menu()

	elif keyboard.is_pressed('l'):
		#put the system into video-game controller mode.
		decision = input('\nPress (y) and enter to activate video-game controller mode. ')
		
		if decision.lower().__eq__('y'):
	
			# Set up HID device
			VENDOR_ID = 0x0079
			PRODUCT_ID = 0x0006
			device = hid.device()
			device.open(VENDOR_ID, PRODUCT_ID)

			print(f"\nCurrent drive speed: {drive_speed}")
			print("Press 'L' again to exit video-game controller mode.")

			# Read data on a non-precise interval timer
			while True:
				if keyboard.is_pressed('l'):
					break

				# Read input report
				report = device.read(64)
				xraw = report[0]
				yraw = report[1]

				#convert to normalized x and y vectors
				x =  (xraw-128)/128
				y = -(yraw-128)/128

				#convert to motor rotations
				M1 =  (x-y) * drive_speed
				M2 = (-x-y) * drive_speed
    
				# Parse the data and print it to the console
				#print(f'Unscaled values: ({xraw}, {yraw})  ' + \
				#		f'Scaled: ({round(x,3)}, {round(y,3)})  ' + \
				#		f'Mot. speed: ({int(M1)}, {int(M2)})')
				controller.send_command(cmds.DUAL_DRIVE, M1, M2)

				
		print("\nExiting.\n\n")
		time.sleep(DWELL)
		menu()
	
		
