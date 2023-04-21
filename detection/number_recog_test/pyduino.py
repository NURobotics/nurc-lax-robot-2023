import serial
import math
from math import acos, atan, cos, sin
import time

def sq(x): return x**2

def convert_coords(init_coords):
    '''Takes the coordinates output by the object detection
    code and converts it into coordinates for the robot to move to.
    '''
    if len(init_coords) == 0:
        return []

    [x,y] = init_coords

    #extents of motion for the CV code
    lx = 20.5
    ly = 15.4
    #extents of motion of the robot
    rx = lx/2
    ry = 13.9

    posn_robot = ly - ry

    #convert x
    x_new = round(x - rx, 2)
    y_new = round(y - posn_robot, 2)

    return [x_new, y_new]

def forward_kinematics(theta1, theta2):
    '''Given a set of angles to rotate the robot to, finds the current position
    of the toolhead in x and y.
    '''

    theta1F = theta1 * math.pi / 180   # degrees to radians
    theta2F = theta2 * math.pi / 180
    xP = L1 * cos(theta1F) + L2 * cos(theta1F + theta2F)
    yP = L1 * sin(theta1F) + L2 * sin(theta1F + theta2F)

    return xP, yP

def inverse_kinematics(x,y):
    '''Given a desired position in (x,y), finds the joint angles
    theta1, theta2 needed to achieve that position. Also calculates
    an angle phi for joint 3 such that the gripper will be parallel
    to the x axis.

    Returns: theta1, theta2, phi
    '''

    #lengths of arms
    L1 = 8.98 #inches
    L2 = 5.61 #inches

    theta2 = acos((sq(x) + sq(y) - sq(L1) - sq(L2)) / (2 * L1 * L2))
    if (x < 0 and y < 0) :
        theta2 = (-1) * theta2
      
    theta1 = atan(x / y) - atan((L2 * sin(theta2)) / (L1 + L2 * cos(theta2)))
  
    theta2 = (-1) * theta2 * 180 / math.pi
    theta1 = theta1 * 180 / math.pi

    # Angles adjustment depending in which quadrant the final tool coordinate x,y is
    if (x >= 0 and y >= 0) :       # 1st quadrant
        theta1 = 90 - theta1
      
    if (x < 0 and y > 0) :       # 2nd quadrant
        theta1 = 90 - theta1
      
    if (x < 0 and y < 0) :       # 3rd quadrant
        theta1 = 270 - theta1
        phi = 270 - theta1 - theta2
        phi = (-1) * phi
      
    if (x > 0 and y < 0) :       # 4th quadrant
        theta1 = -90 - theta1
      
    if (x < 0 and y == 0) :
        theta1 = 270 + theta1
      
  
    # Calculate "phi" angle so gripper is parallel to the X axis
    phi = 90 + theta1 + theta2
    phi = (-1) * phi

    # Angle adjustment depending in which quadrant the final tool coordinate x,y is
    if (x < 0 and y < 0) :       # 3rd quadrant
        phi = 270 - theta1 - theta2
      
    if (abs(phi) > 165) :
        phi = 180 + phi
      
    theta1=round(theta1)
    theta2=round(theta2)
    phi=round(phi)

    return theta1, theta2, phi

def format_commands(j1, j2, j3, z, gripper):
    '''A function to take in data for the stepper motors and gripper
    servo, then convert to a text format that we can use to move the
    motors with the Arduino.

    Assume the 'save program' and 'run program' buttons won't be used
    for this application of the robot, and that speed + accel will be constant.

    Format of data to be written to the Arduino:
        data[0] - SAVE button status
        data[1] - RUN button status
        data[2] - Joint 1 angle
        data[3] - Joint 2 angle
        data[4] - Joint 3 angle
        data[5] - Z position
        data[6] - Gripper value
        data[7] - Speed value
        data[8] - Acceleration value

    Returns: a text version of the list
    '''

    #format should look like "1,2,3,4,5,6,7,8,9" with no brackets/spaces
    data_lst = [0, 0, j1, j2, j3, z, gripper, 500, 500]
    str_data = str(data_lst).replace('[','') \
                .replace(']','') \
                .replace(' ','')

    return str_data




def write_read_arduino(text):
    '''Writes data to the Arduino Serial. Can also read data from the 
    Arduino and return it as text.
    '''

    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
    arduino.write(text.encode())

    time.sleep(0.05)
    data = arduino.readline()
    return data


if __name__ == '__main__':
    
    x = 6.2
    y = 11.3
    theta1, theta2, phi = inverse_kinematics(x,y)
    print('Theta1 and theta2 are: ', theta1, theta2)

    [xnew, ynew] = convert_coords([x,y])
    print('\nXnew and ynew are: ', xnew, ynew)

    print('8 squared is: ', sq(8))