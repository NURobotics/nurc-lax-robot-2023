import cv2
import numpy as np
import imutils
from imutils.video import VideoStream
from collections import deque
import time
import sys

sys.path.append("/Users/samuelhodge/GitHub/nurc-lax-robot-2023/motor_control")

from PyRoboteq import roboteq_commands as cmds
from motor_controller import Controller


# Written by Sam Hodge 
# Updated Spring 2023

# Code to mirror the position of the ball and move the end effector to the corresponding position.


vs = VideoStream(src=0).start()
fps = 30
w = 0

# Initialize the hsv value ranges
orangeLower = (0, 114, 142)
orangeUpper = (9, 235, 255)

# Initialize the point queues with size 10
pts = deque(maxlen=20)
pts_real = deque(maxlen=20)

# Initialize background subtraction
backsub = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

# Sleep to give camera time to warm up
time.sleep(2)

# Pixel to real space transform coefficients. See ./LAX_data 3D_data_vis.py for more information

a_x = 3.80389078
b_x = -15.94367503
c_x = -0.0268761
d_x = 0.03557134
e_x = 0.02424526

a_y = -11.5305074
b_y = 0.0132268653
c_y = 8.15573972
d_y = -315.290387

a_z = 10.97947894
b_z = 10.67078221
c_z = 0.29643814

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

controller = Controller(debug_mode = False, exit_on_interrupt = False)  # Create the controller object
is_connected = controller.connect("/dev/tty.usbmodemC13E847AFFFF1") # connect to the controller (COM9 for windows, /dev/tty/something for Linux)

# Set motor to closed loop mode
motor_mode = 3
controller.send_command(cmds.MOTOR_MODE, motor_mode)


while(1):
    # Get new frame
    frame = vs.read()

    if frame is None:
        break

    # Convert frame to HSV color space. Possible frame resizing goes here too.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get dimensions of the frame.  Operation performed for first frame only.
    while w == 0:
        fshape = frame.shape
        midy = int(fshape[0]/2)
        midx = int(fshape[1]/2)
        w = w+1
    
    # Create gridlines
    cv2.line(frame,(midx,0),(midx,fshape[0]),(0,0,255),2)
    cv2.line(frame,(0,midy),(fshape[1],midy),(0,0,255),2)

    # Create background and color masks
    mask = cv2.inRange(hsv, orangeLower, orangeUpper)
    submask = backsub.apply(frame)
    finalmask = mask & submask

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(finalmask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        t1 = time.time()
        c = max(cnts, key=cv2.contourArea)
        
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        t_fin = time.time()

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
        # update the points queue
        pts.appendleft(((x,y,radius)))

    if len(pts) > 0:
        
        X_pix = pts[0][0]
        Y_pix = pts[0][1]
        R_pix = pts[0][2]

        # units in meters
        X_real = .3048*(a_x*np.arctan(d_x*np.divide(np.subtract(X_pix,951),R_pix)) + b_x*np.arctan(e_x*np.divide(np.subtract(X_pix,951),Y_pix)) + c_x)
        Y_real = .3048*(a_y*np.arctan(b_y*np.divide(Y_pix+d_y,R_pix)) + c_y)
        Z_real = .3048*(a_z*np.divide(b_z,R_pix) + c_z)

       

        # Shift Y coord from the floor datum to the center of the robots frame

        if X_real:
            
            # Shifting Y zero to be at the center of the robot
            Y_real -= 1.115

            # Filter's to make sure that the robot movement is inside of the bounds
            if X_real > 1:
                X_real = 1
            elif X_real < -1:
                X_real = -1

            if Y_real < -0.8:
                Y_real = -0.8
            elif Y_real > 0.8:
                Y_real = 0.8

            # Send to motor control
            x_raw = float(X_real)
            y_raw = float(Y_real)

            # print([x_raw,y_raw])

            if (isfloat(x_raw) and isfloat(y_raw)):
                (x, y) = (float(x_raw), float(y_raw))
                (enc1, enc2) = controller.convert_worldspace_to_encoder_cts(x, y)
                (enc1, enc2) = (round(enc1), round(enc2))

            cmd = f"!P 1 {enc1} _!P 2 {enc2} "
            result = controller.request_handler(cmd) #send_raw_command works the same; this grabs returned data
            print([enc1,enc2])
            print(result)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    t2 = time.time()
    print("Time per detection: " ,t2-t1)

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
            
# close all windows
cv2.destroyAllWindows()