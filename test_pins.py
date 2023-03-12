import RPi.GPIO as GPIO
import time
from PyRoboteq import RoboteqHandler
from PyRoboteq import roboteq_comands as cmds


red_pin = 11
yellow_pin = 12
green_pin = 13
speaker_pin = 15

def toggleStackLight(pin, state):
    if(state):
        GPIO.output(pin, GPIO.HIGH) 
    else:
        GPIO.output(pin, GPIO.LOW) 


def main(): 

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(red_pin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(yellow_pin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(green_pin,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(speaker_pin,GPIO.OUT,initial=GPIO.LOW)
    
    print("Starting. Press ctr C to exit")

    pin = 11
   
    try:
        while True:
            print("Pin ", pin, " is being turned to on.")
            toggleStackLight(pin, True)
            time.sleep(1)
            toggleStackLight(pin, False)
            time.sleep(1)
            pin +=  1
            if(pin == 14):
                pin = 15

            if(pin == 16):
                pin = 11
            

    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()


