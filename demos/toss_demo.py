import cv2
import numpy as np
import imutils
from imutils.video import VideoStream
from collections import deque
import time
import sys
import csv

sys.path.append("/Users/samuelhodge/GitHub/nurc-lax-robot-2023/motor_control")

from PyRoboteq import roboteq_commands as cmds
from motor_controller import Controller

def Prediction(time,N,del_t):
    # time is the time that you want to estimate the ball into the future
    # del_t is the time between detections
    # N is the number of times a prediction should be called over the time range
    timeperN = time/N
    if timeperN > del_t:
        pass
    else:
        print("timeperN < delta_t")
    

    # Transition Matrix (F) based on kinematic equations without acceleration
    kf.transitionMatrix = np.array([[1,0,0,timeperN,0,0],
                                    [0,1,0,0,timeperN,0],
                                    [0,0,1,0,0,timeperN],
                                    [0,0,0,1,0,0],
                                    [0,0,0,0,1,0],
                                    [0,0,0,0,0,1]], np.float32)

    # Control Matrix (B) based on the acceleration matrix set in the predict function                                
    kf.controlMatrix = np.array([[0.5*timeperN**2,0,0],
                                 [0,0.5*timeperN**2,0],
                                 [0,0,0.5*timeperN**2],
                                 [1,0,0],
                                 [0,1,0],
                                 [0,0,1]],np.float32)
    Npred = []

    for i in range(N):
        Npred.append(kf.predict(np.array([[0],
                                          [9.8],
                                          [0]],np.float32)))
    return Npred

def FinalPos(X,Y,Vx,Vy,t):
    Xfin = X + Vx*t
    Yfin = Y + Vy*t

    return [Xfin,Yfin]

def error(X,Y,Z,Vx,Vy,Vz,dt):
    # Given four points calculate the error in the kinematic prediction vs the real data
    Xerr = 0
    Yerr = 0
    Zerr = 0

    for i in range(1,5):
        Xerr += (X[0] + Vx[0]*dt*i) - X[i-1]
        Yerr += (Y[0] + Vy[0]*dt*i - 0.5*9.8*(dt*i)**2) - Y[i-1]
        Zerr += (Z[0] + Vz[0]*dt*i) - Z[i-1]

    Xerravg = Xerr/4
    Yerravg = Yerr/4
    Zerravg = Zerr/4
    totalerr = np.sqrt(Xerravg**2+Yerravg**2+Zerravg**2)
    return totalerr

def quadcheck(X,t):
    Y_vals = []
    t_vals = []
    for i in range(0,4):
        np.polyfit(X[1])

def initKalman():

    # Measurement Matrix (H) based on what values will be observed over time (X,Y,Z)
    kf.measurementMatrix  = np.array([[1,0,0,0,0,0],
                                    [0,1,0,0,0,0],
                                    [0,0,1,0,0,0],
                                    [0,0,0,1,0,0],
                                    [0,0,0,0,1,0],
                                    [0,0,0,0,0,1],],np.float32)   

    # Kalman Matrix R: The measurment Noise Covariance Matrix
    # describes the uncertainty with each measurement may need to update after each measurement
    kf.measurementNoiseCov = np.float32(np.eye(3)*.8)

    # Kalman Matrix Q: The Process Measurment Covariance Matrix
    # describes the uncertainty in the model
    kf.processNoiseCov = np.float32(np.eye(6)*0.01)

def calcVels(arr1,arr2,dt):
    # inputs arr1 = [X1,Y1,Z1], arr2 = [X2,Y2,Z2], dt = time step per detection
    # Where arr1 is the newer detection
    # outputs array of velocites [Vx,Vy,Vz]
    Vx = (arr1[0]-arr2[0])/dt
    Vy = (arr1[1]-arr2[1])/dt
    Vz = (arr1[2]-arr2[2])/dt

    return [Vx,Vy,Vz]

def linear_interpolation(x,t,N):
    # Inputs two data points x and t which are arrays of x the dependant and t the independant 
    # N is the number of data points to interpolate
    # Returns an array of the data points 
    t_step = (t[0]-t[1])/(N+1)
    x_step = (x[0]-x[1])/(N+1)
    x_interp = [x[1]]
    for i in range(0,N):
        temp = t_step + x_interp[i]
        x_interp.append(temp)
    x_interp.append(x[1])
    
    return x_interp

def init_record_data():
    f = open("data.csv",'w')
    f.write("X,Y,Z,Vx,Vy,Vz,t\n")
    f.close()

    
def record_data(pts_real,vel_real,t):
    f = open("data.csv",'a')
    if len(pts_real)>1 and len(vel_real)>1:
        for i in pts_real[0]:
            f.write(str(i)+',')

        for i in vel_real[0]:
            f.write(str(i)+',')
        f.write(str(t)+',')
        f.write('\n')
    f.close()


vs = VideoStream(src=2).start()
fps = 30
w = 0
Ball_Thrown = 0

# Initialize the hsv value ranges
orangeLower = (0, 114, 142)
orangeUpper = (9, 235, 255)

# Initialize the point queues with size 10
pts = deque(maxlen=20)
pts_real = deque(maxlen=20)
vel_real = deque(maxlen=20)

# Initialize background subtraction and Kalman Filter
backsub = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
kf = cv2.KalmanFilter(6,6,3)
initKalman()

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
    
init_record_data()


controller = Controller(debug_mode = False, exit_on_interrupt = False)  # Create the controller object
is_connected = controller.connect("/dev/tty.usbmodemC13E847AFFFF1") # connect to the controller (COM9 for windows, /dev/tty/something for Linux)
t_init = time.time()
while(1):
    t1 = time.time()
    Ball_Thrown = False
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
            """
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
            """

            pts_real.append([X_real,Y_real,Z_real])
           
            #print([enc1,enc2])
            #print(result)

        if len(pts_real)>1:
            vel_real.append(calcVels(pts_real[0],pts_real[1],dt))

    
            if (len(vel_real)>3 and vel_real[0][2] < -10) :#meters/second
                Xcol = []
                Ycol = []
                Zcol = []
                Vxcol = []
                Vycol = []
                Vzcol = []
                for i in range(0,4):
                    Xcol.append(pts_real[i][0])
                    Ycol.append(pts_real[i][1])
                    Zcol.append(pts_real[i][2])
                    Vxcol.append(vel_real[i][0])
                    Vycol.append(vel_real[i][1])
                    Vzcol.append(vel_real[i][2])
             
                err = error(Xcol,Ycol,Zcol,Vxcol,Vycol,Vzcol,dt)
                if err<0.05:
                    Ball_Thrown = True
                    print("Ball Has Been Thrown!!")


    if Ball_Thrown:
        # Send prediction to the motor controller
        if vel_real[0][2] != 0:
            # Find time of flight
            tof = Z_real / vel_real[0][2]
            
            # Find the estimated final position of the ball
            Xfin,Yfin = FinalPos(pts_real[0][0],pts_real[0][1],vel_real[0][0],vel_real[0][1],tof)
            
            # Send to motor control

            x_raw = float(Xfin)
            y_raw = float(Yfin)

                # print([x_raw,y_raw])

            if (isfloat(x_raw) and isfloat(y_raw)):
                (x, y) = (float(x_raw), float(y_raw))
                (enc1, enc2) = controller.convert_worldspace_to_encoder_cts(x, y)
                (enc1, enc2) = (round(enc1), round(enc2))

            cmd = f"!P 1 {enc1} _!P 2 {enc2} "
            result = controller.request_handler(cmd) #send_raw_command works the same; this grabs returned data

    
        
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    t2 = time.time()
    dt = t2-t1
    #print("Time per detection: ",dt)
    record_data(pts_real,vel_real,t2-t_init)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
            
# close all windows
cv2.destroyAllWindows()




    
