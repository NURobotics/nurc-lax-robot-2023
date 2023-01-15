from PyRoboteq import RoboteqHandler
from PyRoboteq import roboteq_commands as cmds
import time
import keyboard 


#extra file I designed to track along a given position

controller = RoboteqHandler()
connected = controller.connect("COM3")

if __name__ == "__main__":
    drive_speed = 0
    #print("Press S to stop")
    #print("Press D to drive")

    track_mode = False
    while connected:

        user_in = input("\nEnter a key to send a command: ")

        if user_in == 'q':
            print("Q pressed")
            print("Stopping motion")
            drive_speed = 0
            controller.send_command(cmds.DUAL_DRIVE, drive_speed, drive_speed)
            
        if user_in == 'x':
            print("X pressed")
            print("Starting to drive")
            drive_speed = 250
            controller.send_command(cmds.DUAL_DRIVE, drive_speed, drive_speed)


        if user_in == 'e':
            #read encoder count
            abscntr_1      = controller.read_value(cmds.READ_ABSCNTR, 1)      # Read encoder counter absolute
            abscntr_2      = controller.read_value(cmds.READ_ABSCNTR, 2)      # Read encoder counter absolute

            print(f"Encoder counts: \nENC1: {abscntr_1} \nENC2: {abscntr_2}")

        if user_in == 'p':
            print("P pressed")
            kp = input("Enter a new value for Kp: ")
            controller.send_command(cmds.KP, kp)

        if user_in == 'i':
            print("I pressed")
            ki = input("Enter a new value for Ki: ")
            controller.send_command(cmds.KI, ki)

        if user_in == 'd':
            print("D pressed")
            kd = input("Enter a new value for Kd: ")
            controller.send_command(cmds.KD, kd)

        if user_in == 'm':
            print("M pressed")
            track_mode = True

            #get position before changes are applied
            abscntr      = controller.read_value(cmds.READ_ABSCNTR, 1)      # Read encoder counter absolute
            print(f"Encoder count: {abscntr}")
            
            #NOTE! In the Roborun+ utility, make sure the Roboteq is currently
            #in "closed loop count position" mode. Other closed loop position modes
            #may work, but this is the tested method as of right now. 
            desired_ct1 = input("Enter desired encoder count for Mot1 (will travel to this): ")
            desired_ct2 = input("Enter desired encoder count for Mot2 (will travel to this): ")

            controller.send_command(cmds.MOT_POS, 1, desired_ct1) # check how this command is supposed to wokr
            controller.send_command(cmds.MOT_POS, 2, desired_ct2) # check how this command is supposed to wokr

            '''
            MOT_POS = "!P" # Go to motor absolute desired position
            MPOS_REL = "!PR" # Go to relative desired position
            NXT_POSR = "!PRX" # NEXT go to relative desired position
            NXT_POS = "PX" # NEXT go to absolute desired position
            '''

        #don't use in this way - this code tries to do position tracking

        #if user_in == 'r':
        #    #reset encoder count to zero
        #    abscntr      = controller.read_value(cmds.READ_ABSCNTR, 1)      # Read encoder counter absolute
        #    print(f"Previous encoder count: {abscntr}")
        #    controller.send_command(cmds.SET_ENC_COUNTER, 1, 0) #first motor; set to zero
        #    abscntr      = controller.read_value(cmds.READ_ABSCNTR, 1)      # Read encoder counter absolute
        #    print(f"New  encoder count: {abscntr}")
        #    input("Press any key to continue.")


        #check if there's a way to display which motor modes are currently active - 
        #want to see if open loop or closed loop
        



        #controller.send_command(cmds.DUAL_DRIVE, drive_speed, drive_speed)
        #battery_amps = controller.read_value(cmds.READ_BATTERY_AMPS, 1) # Read value 1 of battery amps
        #abscntr      = controller.read_value(cmds.READ_ABSCNTR, 1)      # Read encoder counter absolute

        #print(f"Battery amps: {battery_amps}")
        #print(f"Encoder count: {abscntr}") #extra thing added by Sean
            
            

        
        

