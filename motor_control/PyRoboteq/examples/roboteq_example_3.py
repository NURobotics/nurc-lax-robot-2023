from PyRoboteq import RoboteqHandler
from PyRoboteq import roboteq_commands as cmds
import time
import keyboard # to run this library you need to be on root (run this python script as sudo)

controller = RoboteqHandler()
connected = controller.connect("COM3") # Insert your COM port (for windows) or /dev/tty{your_port} (Commonly /dev/ttyACM0) for linux.

if __name__ == "__main__":
    drive_speed = 0
    print("Press S to stop")
    print("Press D to drive")
    while connected:
        
        if keyboard.is_pressed('s'):
            #print("S pressed")
            drive_speed = 0
            
        if keyboard.is_pressed('d'):
            #print("D pressed")
            drive_speed = 250

        
        controller.send_command(cmds.DUAL_DRIVE, drive_speed, drive_speed)
        battery_amps = controller.read_value(cmds.READ_BATTERY_AMPS, 1) # Read value 1 of battery amps
        abscntr      = controller.read_value(cmds.READ_ABSCNTR, 1)      # Read encoder counter absolute

        print(f"Battery amps: {battery_amps}")
        print(f"Encoder count: {abscntr}") #extra thing added by Sean
            
            

        
        

