#from PyRoboteq import RoboteqHandler
from motor_controller import Controller
from PyRoboteq import roboteq_commands as cmds
from control_gui_helpers import *
#import keyboard
import time
import sys
import os

#for visual GUI
curr_dir = os.path.dirname(os.getcwd())
new_dir = curr_dir + '\\motor_control\\python_gui\\code'
sys.path.append(new_dir)



#------------------------------------------------#

controller = Controller(debug_mode = False, exit_on_interrupt = False)  # Create the controller object
#is_connected = controller.connect("/dev/tty.usbmodemC13E847AFFFF1")
is_connected = controller.connect("COM4")

# connect to the controller:
# 1) COM9 for windows
# 2) /dev/tty/.* for Linux/Unix, and find the USB port it's actually connected to using trial/error)


if (not is_connected):
	raise Exception("Error in connection")

#--------------------------#
controller.send_command(cmds.MOTOR_MODE, motor_mode)

# menu loop
menu()
while not has_quit:

	user_cmd = input("\nEnter a command: ")

	if user_cmd.lower() == ('w'):
		print("\nEntering open-loop WASD mode." + \
			"\nPress WASD for u/d/l/r motion and 1234 for ur/dl/ul/dr motion." + \
			"\nPress 'q' to quit.")
		try:
			import keyboard
		except:
			raise Exception("Motor controller: keyboard library not imported correctly; \n" + \
							"This is a known issue with Mac and Linux OS.")

		def key_responder(key):
			''' A brief format for how the program should respond to a keypress of WASD,1234.
			'''
			M1, M2 = drive_speeds_dict[key]	
			while keyboard.is_pressed(key):
				#wait until user is done sending commands
				controller.send_command(cmds.DUAL_DRIVE, M1, M2)
			controller.send_command(cmds.DUAL_DRIVE, 0, 0)   


		while (1):
			if keyboard.is_pressed('w'): key_responder('w')
			if keyboard.is_pressed('a'): key_responder('a')
			if keyboard.is_pressed('s'): key_responder('s')
			if keyboard.is_pressed('d'): key_responder('d')
			if keyboard.is_pressed('1'): key_responder('1')
			if keyboard.is_pressed('2'): key_responder('2')
			if keyboard.is_pressed('3'): key_responder('3')
			if keyboard.is_pressed('4'): key_responder('4')
			
			if keyboard.is_pressed('q'): break

		print('\nQuitting.\n\n')
		time.sleep(DWELL)
		menu()

	###

	elif user_cmd.lower() == ('q'):

		print('\nExiting client\n\n')
		has_quit = True # exit client
		# be sure to close the port
		#ser.close() 

	###

	elif user_cmd.lower() == ('c'):

		print('\nHitting emergency stop \n\n')
		controller.send_command(cmds.EM_STOP) # this will send 0 argument command for emergency stop
		estop_active = True
		#has_quit = True; # exit client
		time.sleep(DWELL)
		menu()

	elif user_cmd.lower() == ('x'):

		print('\nReleasing emergency stop \n\n')
		controller.send_command(cmds.REL_EM_STOP)
		estop_active = False

		time.sleep(DWELL)
		menu()

	###

	elif user_cmd.lower() == ('e'):

		abscntr_1      = (controller.read_value(cmds.READ_ABSCNTR, 1))      # Read encoder counter absolute
		abscntr_2      = (controller.read_value(cmds.READ_ABSCNTR, 2))      # Read encoder counter absolute
		#abscntr_1 = int(abscntr_1.split('=')[-1])
		#abscntr_2 = int(abscntr_2.split('=')[-1])

		print(f"\nEncoder counts: \nENC1: {abscntr_1} \nENC2: {abscntr_2} \n\n")
		time.sleep(DWELL)
		menu()

	###

	elif user_cmd.lower() == ('f'):

		abscntr_1 = (controller.read_value(cmds.READ_ABSCNTR, 1))      # Read encoder counter absolute
		abscntr_2 = (controller.read_value(cmds.READ_ABSCNTR, 2))      # Read encoder counter absolute
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

	elif user_cmd.lower() == ('h'):
		
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


	elif user_cmd.lower() == ('z'):

		if motor_mode != 3:
			print("\nSet Roboteq to Closed Loop Count Position first; will not execute.\n\n")
		else:
			print("\nGoing to position (0,0):\n\n")
			cmd = "!P 1 0 _!P 2 0 "
			result = controller.request_handler(cmd) #send_raw_command works the same; this grabs returned data
			print(result)

		time.sleep(DWELL)
		menu()

	elif user_cmd.lower() == ('u'):
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

	elif user_cmd.lower() == ('i'):
		#getter
		print("\nValid operating modes:")
		for x in modes_dict_text.keys():
			print(f"{x}: {modes_dict_text[x]}")

		op_mode1_raw = controller.read_value(cmds.READ_MMODE, 1)
		op_mode2_raw = controller.read_value(cmds.READ_MMODE, 2)
		print(f"\nOperating modes: \nM1: {op_mode1_raw} \nM2: {op_mode2_raw} \n\n")

		time.sleep(DWELL)
		menu()

	elif user_cmd.lower() == ('r'):
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
					#controller.send_command(cmds.MOT_POS, 1, enc1)
					#controller.send_command(cmds.MOT_POS, 2, enc2)
					#controller.send_command(cmds.MOT_POS, 1, enc1)
					#controller.send_command(cmds.NXT_POS, 2, enc2)

					cmd = f"!P 1 {enc1} _!P 2 {enc2} "
					result = controller.request_handler(cmd) #send_raw_command works the same; this grabs returned data
					print(result)
					break

				else:
					print("\nInvalid input; both numbers must be signed ints.")

		time.sleep(DWELL)
		menu()

	elif user_cmd.lower() == ('t'):
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
					(enc1, enc2) = controller.convert_worldspace_to_encoder_cts(x, y) # IMMPORTANT
					(enc1, enc2) = (round(enc1), round(enc2)) # Important

					print(f"\nEncoder counts calculated to go to: \nENC1: {enc1} \nENC2: {enc2}")
					break

				else:
					print("\nInvalid input; both numbers must be floats.")

			decision = input("\nEnter 'y' to go to these encoder counts. ")
			if 'y'.__eq__(decision.lower()):
				print("\nSetting encoder counts.\n\n")
				#controller.send_command(cmds.MOT_POS, 1, enc1)
				#controller.send_command(cmds.MOT_POS, 2, enc2)``
				#controller.send_command(cmds.MOT_POS, 1, enc1)
				#controller.send_command(cmds.NXT_POS, 2, enc2)
				cmd = f"!P 1 {enc1} _!P 2 {enc2} " # Important
				result = controller.request_handler(cmd) #send_raw_command works the same; this grabs returned data # Important
				print(result)

		time.sleep(DWELL)
		menu()

	elif user_cmd.lower() == ('m'):
		#get motor speed
		print(f"\nMotor speed (0-1000): {drive_speed} \n\n")

		time.sleep(DWELL)
		menu()

	elif user_cmd.lower() == ('n'):
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

	elif user_cmd.lower() == ('l'):
		#put the system into video-game controller mode.
		decision = input('\nPress (y) and enter to activate video-game controller mode. ')
		
		if decision.lower().__eq__('y'):
	
			#for PS controller
			try:
				import hid
			except:
				raise Exception("Motor control GUI: run 'pip install hid' to access this command")

			# Set up HID device
			VENDOR_ID = 0x0079
			PRODUCT_ID = 0x0006
			device = hid.device()
			try:
				device.open(VENDOR_ID, PRODUCT_ID)
			except:
				print("\nCould not connect to controller. Exiting.\n\n")
				continue

			print(f"\nCurrent drive speed: {drive_speed}")
			print("Press 'Start' or 'Select' on controller to exit video-game controller mode.")

			# Read data on a non-precise interval timer
			while True:
				#if keyboard.is_pressed('l'):
				#	break

				# Read input report
				report = device.read(64)
				xraw = report[0]
				yraw = report[1]
				start_select = report[6]

				if (start_select != 0): 
					controller.send_command(cmds.DUAL_DRIVE, 0, 0)   
					break

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

	elif user_cmd.lower() == ('k'):

		kp, kd, ki = input("Enter kp, kd, and ki: \n").split()
		controller.set_pid_params(kp, kd, ki)

		print(f"\nNew kp: {kp}")
		print(f"New kd: {kd}")
		print(f"New ki: {ki} \n")

		controller.read_PID()

		time.sleep(DWELL + 1)
		menu()

	elif user_cmd.lower() == 'a':

		pid = controller.read_PID()

		kp = pid[0][0]
		ki = pid[1][0]
		kd = pid[2][0]

		print(f"Current Kp = {kp} \nCurrent Ki = {ki} \n Current Kd = {kd}")

		time.sleep(DWELL)
		menu()

	elif user_cmd.lower() == ('p'):

		accel, decel, max_v = input("Enter max closed-loop acceleration, closed-loop deceleration, "
									"and closed-loop velocity: \n").split()
		controller.set_kinematics_params(accel, decel, max_v)

		print(f"\nNew closed-loop max acceleration: {accel}")
		print(f"New closed-loop max deceleration: {decel}")
		print(f"New closed-loop max velocity: {max_v} \n")

		time.sleep(DWELL + 2)
		menu()


	elif user_cmd.lower() == ('b'):

		print("\nFormat of common commands to send to the Roboteq: \n" + \
				"!<RUNTIME_COMMAND> <CHANNEL> <VALUE> (ex: !G 1 100) or\n" + \
				"?<RUNTIME_QUERY> <CHANNEL> (ex: ?C 1) \n" + \
				"Other commands, like % and ^ commands, can be dangerous to execute - be careful.")

		cmd = input('\nEnter a command to send to the Roboteq (q to exit). ')
		if cmd.lower() == 'q':
			pass

		#there are more validation tests to do for the command, but this will be a start
		elif cmd[0] in ["!","?","^"]: #and len(cmd.split(' ')) in [2, 3]:

			#this method is limited but produces results. we want the ability to send more than 1 line at once using "_"
			'''
			if "?" in cmd[0]:
				rcvd = controller.read_value(*cmd.split(' '))
				print(rcvd)

			else:
				controller.send_command(*cmd.split(' '))
			'''
			if cmd[-1] != " ":
				cmd = cmd + " "

			result = controller.request_handler(cmd) #send_raw_command works the same; this grabs returned data
			print(result)

		else:
			print("Invalid command; exiting.\n")

		print()
		time.sleep(DWELL)
		menu()

	elif user_cmd.lower() == ('g'):


		from python_gui.code.GUI import GUI, init_gui
		from python_gui.code.geometry import win_height, win_width
		
		if motor_mode != 3:
			print("\nSet Roboteq to Closed Loop Count Position first; will not execute.\n\n")
		else:
			print("\nStarting visual GUI:\n")
			gui = GUI(win_height, win_width, "../media/lax_goalie_diagram.png", controller) #namespace for variables: geometry.py
			init_gui(gui)
			while True:
				#allow user to use this infinitely
				pass
		
		time.sleep(DWELL)
		menu()
	
		
