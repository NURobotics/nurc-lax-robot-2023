from PyRoboteq import RoboteqHandler
from PyRoboteq import roboteq_commands as cmds

DRIVE_SPEED = 100
DWELL = 0.5 #time between commands
has_quit = False
enc_count = None

menu_text = \
	'\tROBOTEQ MOTOR DRIVER INTERFACE \n' + \
	'\tWASD keys: move up/down/left/right \n' + \
	'\te: read encoder position (counts) \th: set current posn as home \n' + \
	'\tq: quit client \tc: ESTOP'

controller = RoboteqHandler(debug_mode = True, exit_on_interrupt = False)  # Create the controller object
is_connected = controller.connect("COM3") # connect to the controller (COM9 is an example for windows)

#-----------------------------#

if (not is_connected):
    raise Exception("Error in connection")

# menu loop
while not has_quit:

	## display the menu options; this list will grow
	#print('\tb: read current (mA) \tc: read encoder (counts) \td: read encoder (deg)')
	#print('\te: reset encoder \tf: set PWM, -100 to 100 \tg: set current gains')
	#print('\th: get current gains \ti: set position gains \t\tj: get position gains')
	#print('\tk: test current gains \tl: go to position \t\tm: load step traj.')
	#print('\tn: load cubic traj. \to: execute traj. \t\tp: power off PWM')
	#print('\t' + '_' * 90)
	#print('\tq: quit \t\tr: read PIC32 mode \t\ty: view traj. arrays\n')

	#ser.flush()

	## read the user's choice
	#selection = input('ENTER COMMAND: ')
	#selection_endline = selection+'\n'
	 
	## send the command to the PIC32
	#ser.write(selection_endline.encode()); # .encode() turns the string into a char array

	# take the appropriate action
	# there is no switch() in python, using if elif instead


	#Menuing: use keyboard.is_pressed() to detect instant input

	if keyboard.is_pressed('w'):

		#send commands to move up
		while keyboard.is_pressed('w'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, -DRIVE_SPEED, DRIVE_SPEED)

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)   

	###

	elif keyboard.is_pressed('s'):

		#send commands to move down
		while keyboard.is_pressed('s'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, DRIVE_SPEED, -DRIVE_SPEED)

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)  

	###

	elif keyboard.is_pressed('a'):

		#send commands to move left
		while keyboard.is_pressed('a'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, DRIVE_SPEED, DRIVE_SPEED)

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)  

	###

	elif keyboard.is_pressed('d'):

		#send commands to move right
		while keyboard.is_pressed('d'):
			#wait until user is done sending commands
			controller.send_command(cmds.DUAL_DRIVE, -DRIVE_SPEED, -DRIVE_SPEED)

		controller.send_command(cmds.DUAL_DRIVE, 0, 0)  

	###

	elif keyboard.is_pressed('q'):

		print('Exiting client')
		has_quit = True; # exit client
		# be sure to close the port
		#ser.close() 

	###

	elif keyboard.is_pressed('c'):

		print('Hitting emergency stop')
		controller.send_command(cmds.EM_STOP) # this will send 0 argument command for emergency stop
		has_quit = True; # exit client

	###

	elif keyboard.is_pressed('e'):

		#controller.send_command(cmds.EM_STOP) # this will send 0 argument command for emergency stop
		enc_count = controller.read_value(cmds.READ_ABSCNTR, 1)
		print(f"Current encoder count: {enc_count}")
		time.sleep(DWELL)
		print(menu_text)

	###

	elif keyboard.is_pressed('h'):
		
		if not enc_count:
			print("We need to set an encoder position first.")
		else:
			print("Setting current position as home position: {enc_count}")
			controller.send_command(cmds.HOME_COUNTER, enc_count)

		time.sleep(DWELL)
		print(menu_text)


	'''
	if (selection == 'b'):

		bytes = ser.read_until(b'\n')
		current = float(bytes)
		print(f'Current reading: {current} \n')

	elif (selection == 'c'):

		#bytes = ser.read_until(b'\n')
		#count = int(bytes)
		#print(f'Encoder reading: {count} \n')
		pass

	elif (selection == 'd'):

		#bytes = ser.read_until(b'\n')
		#degs = float(bytes)
		#print(f'Encoder reading (degrees) {degs} \n')	
		pass

	elif (selection == 'e'):
		#no data to read here; just sends data to the PICO
		#print('Sent command to reset the encoder count.\n')
		pass

	elif (selection == 'f'):
		
		#pwm = input('Enter a new value for PWM (-100 to 100): ')
		#serial_text = (str(pwm) + '\n').encode()
		#ser.write(serial_text)
		#print(f'New value of PWM: {pwm} \n')


	elif (selection == 'g'):

		##enter new values of position gains
		#gain = input('Enter new gain Kp for current: ')
		#gain = float(gain)
		#serial_text = (str(gain) + '\n').encode()
		#ser.write(serial_text)

		#gain = input('Enter new gain Ki for current: ')
		#gain = float(gain)
		#serial_text = (str(gain) + '\n').encode()
		#ser.write(serial_text)
		#print()

	elif (selection == 'h'):

		##read values of current gains from UART
		#bytes = ser.read_until(b'\n')
		#gain = float(bytes)
		#print(f'Value of current gain Kp: {gain}')

		#bytes = ser.read_until(b'\n')
		#gain = float(bytes)
		#print(f'Value of current gain Ki: {gain}\n')

	elif (selection == 'i'):

		##set new values of position gains
		#gain = input('Enter a new value for position gain Kp: ')
		#gain = float(gain)
		#serial_text = (str(gain) + '\n').encode()
		#ser.write(serial_text)

		#gain = input('Enter a new value for position gain Ki: ')
		#gain = float(gain)
		#serial_text = (str(gain) + '\n').encode()
		#ser.write(serial_text)

		#gain = input('Enter a new value for position gain Kd: ')
		#gain = float(gain)
		#serial_text = (str(gain) + '\n').encode()
		#ser.write(serial_text)
		#print()
		pass

	elif (selection == 'j'):

		#read values of position gains from UART
		#bytes = ser.read_until(b'\n')
		#gain = float(bytes)
		#print(f'Value of position gain Kp: {gain}')

		#bytes = ser.read_until(b'\n')
		#gain = float(bytes)
		#print(f'Value of position gain Ki: {gain}')

		#bytes = ser.read_until(b'\n')
		#gain = float(bytes)
		#print(f'Value of position gain Kd: {gain} \n')	
		pass


	elif (selection == 'k'):

		#print('Running ITEST mode now. Check plot of datapoints.')
		#ref_array, curr_array = read_arrays()
		#plot_arrays(ref_array, curr_array)
		pass

	elif (selection == 'l'):
		
		##go to a position
		#posn = input('Enter a position to move to: ')
		#posn = float(posn)
		#serial_text = (str(posn) + '\n').encode()
		#ser.write(serial_text)
		#print()

		#PIC handles the rest from here
		pass

	elif (selection == 'm'):
		#send_trajectory('step')
		pass

	elif (selection == 'n'):
		#send_trajectory('cubic')
		pass

	elif (selection == 'o'):
		pass
		#print('Executing trajectory...')
		#traj_list, posn_list = read_arrays()
		#plot_arrays(traj_list, posn_list)

	elif (selection == 'p'):
		#print("PIC mode set to IDLE.\n")
		pass

	elif (selection == 'r'):
		pass

	elif (selection == 'y'):
		pass

	elif (selection == 'q'):
		print('Exiting client')
		has_quit = True; # exit client
		# be sure to close the port
		ser.close()

	else:
		print('Invalid Selection ' + selection_endline)

	'''



