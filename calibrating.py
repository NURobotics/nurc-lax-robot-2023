from PyRoboteq import RoboteqHandler
from PyRoboteq import roboteq_commands as cmds
import RPi.GPIO as GPIO
import time

topSensor = 12
bottomSensor = 13
rightSensor = 16
leftSensor = 15


CALIBRATESPEED = 50

drive_speed_motor_one = 0
drive_speed_motor_two = 0

# def moveUp():
#     controller.send_command(cmds.DUAL_DRIVE, CALIBRATESPEED, -CALIBRATESPEED)

# def moveDown():
#     controller.send_command(cmds.DUAL_DRIVE, -CALIBRATESPEED, CALIBRATESPEED)

# def moveRight():
#     controller.send_command(cmds.DUAL_DRIVE, CALIBRATESPEED, CALIBRATESPEED)

# def moveLeft():
#     controller.send_command(cmds.DUAL_DRIVE, -CALIBRATESPEED, -CALIBRATESPEED)


# def stopMotors():
#     controller.send_command(cmds.DUAL_DRIVE, 0, 0)


controller = RoboteqHandler(debug_mode=False, exit_on_interrupt=False) 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(topSensor,GPIO.IN)
GPIO.setup(bottomSensor,GPIO.IN)
GPIO.setup(leftSensor,GPIO.IN)
GPIO.setup(rightSensor,GPIO.IN)

connected = controller.connect("/dev/ttyACM0") # Insert your COM port (for windows) or /dev/tty{your_port} (Commonly /dev/ttyACM0) for linux.

#   Moves the robot to the top or bottom of bar
#   negative speed moves down
def moveToVerticalBar(speed):
    if speed > 0:
        sensor = rightSensor
        print("Moving up")
    else:
        sensor = leftSensor
        print("Moving down")
    while connected & GPIO.input(sensor) == GPIO.LOW:
        #print("Turning Motors")
        controller.send_command(cmds.DUAL_DRIVE, -speed, speed)
        
    controller.send_command(cmds.DUAL_DRIVE, 0, 0)   



#   Moves the robot to the right or left
#   negative speed moves left
def moveToHorizontalBar(speed):
    
    if speed > 0:
        sensor = topSensor
        print("Moving right")
    else:
        sensor = bottomSensor
        print("Moving left")
    while connected & GPIO.input(sensor) == GPIO.LOW :
        
        controller.send_command(cmds.DUAL_DRIVE, -speed, -speed)
        
    controller.send_command(cmds.DUAL_DRIVE, 0, 0)   



if __name__ == "__main__":
    time.sleep(2)
    moveToHorizontalBar(-CALIBRATESPEED)
    moveToVerticalBar(-CALIBRATESPEED)

    #controller.send_command(cmds.SET_ENC_COUNTER, 0, 0)
    #moveToVerticalBar(CALIBRATESPEED)
    #vertDist = controller.read_value(cmds.READ_ABSCNTR, 1)
    #print(vertDist)

    #moveToHorizontalBar(CALIBRATESPEED)
    #horizDist = controller.read_value(cmds.READ_ABSCNTR, 1)
    #controller.send_command(cmds.SET_ENC_COUNTER, 0, 0)
    #print(horizDist)
        
            
            

        
        
