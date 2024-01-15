from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import matplotlib.pyplot as plt



ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
ap.add_argument("-dd","--depth",type=int, default=0,
	help="Depth data for calibration: Enter a 1 to collect data to csv file. Set to not use background subtraction mask")
ap.add_argument("-d", "--data", type=int, default=0,
	help="Record all position, velocity, and acceleration data. Enter a 1 to enable")
ap.add_argument("-p", "--plot", type=int, default=0,
	help="Create plot of the radius over time. Enter a 1 to enable")
args = vars(ap.parse_args())
def colordetec():

	# define the lower and upper boundaries of the "orange"
	# Orange Lower for Logitech webcam (0,210,255)
	# Orange upper for Logitech webcam (6,255,255)
	# Orange lower for ping pong testing (10, 149, 138)
	# Orange upper fo ping pong testing (18, 255, 255)
	orangeLower = (0,210,255)
	orangeUpper = (6,255,255)

	# Initialize the points queue
	pts = deque(maxlen=args["buffer"])
	pts_real = deque(maxlen=args["buffer"])
	vel = deque(maxlen=args["buffer"])
	accel = deque(maxlen=args["buffer"])
	# if a video path was not supplied, grab the reference
	# to the webcam
	if not args.get("video", False):
		vs = VideoStream(1).start()
	# otherwise, grab a reference to the video file
	else:
		vs = cv2.VideoCapture(args["video"])
	# allow the camera or video file to warm up
	time.sleep(2.0)	

	w=0
	radius_list = []
	backsub = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
	t_init = time.time()
	# keep looping
	while True:
		t0 = time.time()
		# grab the current frame
		frame = vs.read()
		# handle the frame from VideoCapture or VideoStream
		frame = frame[1] if args.get("video", False) else frame
		# if we are viewing a video and we did not grab a frame,
		# then we have reached the end of the video
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

		# construct a mask for the color "orange", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask
		mask = cv2.inRange(hsv, orangeLower, orangeUpper)
		submask = backsub.apply(frame)
		# mask = cv2.erode(mask, None, iterations=2)
		# mask = cv2.dilate(mask, None, iterations=2)
		
		# If collecting depth data only use the color mask. Otherwise do a bitwise and operation with the color mask and the background subtraction mask
		if args["depth"]:
			finalmask = mask
		else:
			finalmask = mask & submask

		# find contours in the mask and initialize the current
		# (x, y) center of the ball
		cnts = cv2.findContours(finalmask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		center = None
		# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			
			((x, y), radius) = cv2.minEnclosingCircle(c)
			t_fin = time.time()

			# only proceed if the radius meets a minimum size
			if radius > 1:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 255), 2)
			# update the points queue
			pts.appendleft(((int(x),int(y),radius)))
			if args["plot"]:
				radius_list.append((radius,t_fin-t_init))

		## Moving Robotic arm
		# Perhaps make a transform for the position of the ball on the screen to the position of the ball to the robot
		# First normalize the center quanities to start at the center of the image
		# The catcher should start off in the center of the goal
		
		# Transform from pixel space to real space
		if len(pts)>2:
			X_real = 5.7970*np.pi/np.arctan(pts[0][2]/(pts[0][0]-midx))/180
			Y_real = 5.8937*np.pi/np.arctan(pts[0][2]/(midy-pts[0][1]))/180
			Z_real = 100.1/pts[0][2] + 0.2939
			pts_real.appendleft((X_real,Y_real,Z_real,time.time()-t_init))
			
			# Derive Velocities
			if len(pts_real)>2 and (pts_real[0][3]!=pts_real[1][3]):
				Vx = (pts_real[0][0]-pts_real[1][0])/(pts_real[0][3]-pts_real[1][3])
				Vy = (pts_real[0][1]-pts_real[1][1])/(pts_real[0][3]-pts_real[1][3])
				Vz = (pts_real[0][2]-pts_real[1][2])/(pts_real[0][3]-pts_real[1][3])
			else:
				Vx = 0
				Vy = 0
				Vz = 0
					
			vel.appendleft((Vx,Vy,Vz,pts_real[0][3]))

			if len(vel)>2 and vel[0][3]!=vel[1][3]:
				Ax = (vel[0][0]-vel[1][0])/(vel[0][3]-vel[1][3])
				Ay = (vel[0][1]-vel[1][1])/(vel[0][3]-vel[1][3])
				Az = (vel[0][2]-vel[1][2])/(vel[0][3]-vel[1][3])
			else:
				Ax=0
				Ay=0
				Az=0
			
			accel.appendleft((Ax,Ay,Az,vel[0][3]))

			posstring = "X=%.3f, Y=%.3f, Z=%.3f" % (X_real,Y_real,Z_real)
			velstring = "Vx=%.3f, Vy=%.3f, Vz=%.3f" % (vel[0][0],vel[0][1],vel[0][2])
			accelstring = "Ax=%.3f, Ay=%.3f, Az=%.3f" % (accel[0][0],accel[0][1],accel[0][2])
				
			cv2.putText(frame,posstring,(50,25),cv2.FONT_HERSHEY_COMPLEX,.5,(0,255,0))
			cv2.putText(frame,velstring,(50,50),cv2.FONT_HERSHEY_COMPLEX,.5,(0,255,0))
			cv2.putText(frame,accelstring,(50,100),cv2.FONT_HERSHEY_COMPLEX,.5,(0,255,0))
		
			if args["data"]:
				f = open('alldata.csv','a')
				f.write(str(pts_real[0][0])+','+str(pts_real[0][1])+','+str(pts_real[0][2])+','+str(pts_real[0][3])+','+str(vel[0][0])+','+str(vel[0][1])+','+str(vel[0][2])+','+str(vel[0][3])+','+str(accel[0][0])+','+str(accel[0][1])+','+str(accel[0][2])+','+str(accel[0][3]))
				f.write('\n')
				f.close()
	
		# Calculate the FPS and print to frame
		t1 = time.time()
		FPS = "FPS:"+ str(int(1/(t1-t0)))
		cv2.putText(frame,FPS,(fshape[1]-100,50),cv2.FONT_HERSHEY_COMPLEX,.5,(0,255,0))

		# Collect data in order to calibrate the range as a function of x, y, and r 
		# Must have background subtraction turned off
		if args["depth"]:
			key = cv2.waitKey(1)
			if key == ord('a'):
				f = open('depth_data.csv','a')
				temp = input("Input the Z coordinate: ")
				f.write(str(pts[0][0]) + ',' + str(pts[0][1]) + ',' + str(pts[0][2])+ ',' + temp)
				f.write('\n')
				f.close()
				print('Data Recorded!\n')

		# show the frame to our screen
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		# if the 'q' key is pressed, stop the loop
		if key == ord("q"):
			break

	# if we are not using a video file, stop the camera video stream
	if not args.get("video", False):
		vs.stop()
	# otherwise, release the camera
	else:
		vs.release()
	# close all windows
	cv2.destroyAllWindows()

	# Plot the radius over time
	if args["plot"]:
		for i in radius_list:
			plt.plot(i[1],i[0],'ro')
		plt.title('Radius over time')
		plt.grid()
		plt.show()
	

	return(pts)

colordetec()
