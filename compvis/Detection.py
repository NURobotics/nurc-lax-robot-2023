import cv2
import imutils
import time
import numpy as np
import glob
import pickle
import os
from linetimer import CodeTimer


class Cam():
    # Class to initialize webcams and output the position of the ball in the frame. 
    # Begin by initializing the class with no inputs.
    # Use find_camera_id to get the find the correct webcam


    def __init__(self, camID = None):
        self.cap = None
        self.frame = None
        self.hsv_value = None
        self.orange_upper = np.array([18, 255, 255])
        self.orange_lower = np.array([10, 149, 138])
        self.window = None
        self.camID = camID
        self.x = None 
        self.y = None
        self.R = None
        self.fps = None
        # Height and Width of the frame in pixels
        self.W = None
        self.H = None
    
    def find_camera_id(self):
        # Loop over camera ID's and display their outputs to the user to make sure the you have the correct webcam. Make sure to know what camera is what
        # If you see the videostream you are looking for press s and the the camID will be saved to the class. If you want to move to the next id press q. 
        # TODO: Fix bug where if there is no camera 




        for cam_id in range(2):  # Adjust the range based on the number of cameras you want to check
            cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
            if not cap.isOpened():
                print(f"Camera ID {cam_id} is not available.")
                continue
            
            print("Press s to use displayed camera.\nPress q to skip to the next camera.")

            while True:
                ret, frame = cap.read()
                if not ret:
                    print(f"Failed to retrieve frame from Camera ID {cam_id}.")
                    break

                cv2.imshow(f"Camera ID {cam_id}", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('s'):
                    self.camID = cam_id
                    self.cap = cap
                    self.window = (f'Cam {self.camID}')
                    self.H = np.shape(frame)[0]
                    self.W = np.shape(frame)[1]
                    print(f'--> Camera Index: [{self.camID}] saved!\n')
                    cv2.destroyAllWindows()
                    return
                    
                if key == ord('q'):
                    print("--> Camera skipped!")
                    break
                


            cap.release()
            cv2.destroyAllWindows()
        
        pass
    
    
    def set_camera_id(self):
        cam_id = self.camID
        cap = cv2.VideoCapture(self.camID, cv2.CAP_DSHOW)
        if not cap.isOpened():
            print(f"Camera ID {cam_id} is not available.")
        
        print("Press s to use displayed camera.\nPress q to skip to the next camera.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"Failed to retrieve frame from Camera ID {cam_id}.")
                break

            cv2.imshow(f"Camera ID {cam_id}", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                self.camID = cam_id
                self.cap = cap
                self.window = (f'Cam {self.camID}')
                self.H = np.shape(frame)[0]
                self.W = np.shape(frame)[1]
                print(f'--> Camera Index: [{self.camID}] saved!\n')
                cv2.destroyAllWindows()
                return
                
            if key == ord('q'):
                print("--> Camera skipped!")
                break
            


        cap.release()
        cv2.destroyAllWindows()
        
        pass
    
        
    def get_frame(self):
        # Outputs the frame from the cap object
        ret,frame = self.cap.read()
        if ret:
            self.frame = frame
        else:
            self.frame = None

    def show_frame(self):
        if self.x and self.y and self.R:
            cv2.circle(self.frame, (int(self.x), int(self.y)), int(self.R), (0, 255, 255), 2)

        if self.fps:
            cv2.putText(self.frame, str(self.fps), (self.W - 100, 50), 0, 1, (0, 255, 0), 2)

        cv2.imshow(self.window,self.frame)

    def print_ball_pos(self):
        if self.x and self.y and self.R:
            print(self.x, self.y, self.R)

    def get_hsv_ranges(self):
        # TODO: Fix bug (Bug occurs when then there is no camera selected from find_cam_id) --> Exit if there is no camera initialized
        # TODO: Fix bug where reseting the range does not fully reset the hsv ranges

        def get_hsv_range(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                print(f'--> HSV values recorded')
                hsv_pixel = hsv_frame[y, x]
                lower_hsv = np.array([hsv_pixel[0] - 10 , hsv_pixel[1] - 10, hsv_pixel[2] - 10])
                upper_hsv = np.array([hsv_pixel[0] + 10, hsv_pixel[1] + 10, hsv_pixel[2] + 10])
                

                # Make sure that hsv values fall into the proper ranges
                for i in range(len(lower_hsv)):
                    if lower_hsv[i] < 0:
                        lower_hsv[i] = 0
                    if upper_hsv[0] > 179:
                        upper_hsv[0] = 179
                    if upper_hsv[1]> 255 :
                        upper_hsv[1] = 255
                    if upper_hsv[2] > 255 :
                        upper_hsv[2] = 255

                
                self.hsv_value = lower_hsv, upper_hsv
        
        hsv_values = []

        highest_hsv = np.array([0, 0, 0])
        lowest_hsv = np.array([180, 255, 255])
        hsv_limits = [lowest_hsv, highest_hsv]
        cv2.namedWindow('Video Stream')
        cv2.setMouseCallback('Video Stream', get_hsv_range)
        print("Click on the Video Stream frame until the mask looks correct.\nPress s to save hsv bounds.\nPress r to reset mask.\nPress q to exit")
        while True:
            self.get_frame()
             # Convert the frame to the HSV color space
            hsv_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)


            if self.hsv_value:

                if np.any(np.isin(self.hsv_value, hsv_values, invert=True)): # inserts a new hsv_value into the array if it is not already in the array
                    hsv_values.append(self.hsv_value) 
                
                lowest_hsv = np.array([min(lowest_hsv[0], self.hsv_value[0][0]),min(lowest_hsv[1], self.hsv_value[0][1]), min(lowest_hsv[2], self.hsv_value[0][2])])
                highest_hsv = np.array([max(highest_hsv[0], self.hsv_value[1][0]),max(highest_hsv[1], self.hsv_value[1][1]), max(highest_hsv[2], self.hsv_value[1][2])])
                    
                mask = cv2.inRange(hsv_frame, lowest_hsv, highest_hsv)
                #result = cv2.bitwise_and(self.frame, self.frame, mask=mask)
                mask_inv = cv2.bitwise_not(mask)
                result = cv2.bitwise_and(self.frame,self.frame, mask=mask_inv)
                cv2.imshow('Video Stream', result)
                
            if self.hsv_value is None:
                cv2.imshow('Video Stream', self.frame)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                print(f'--> Orange Lower for {self.window}: {lowest_hsv}')
                print(f'--> Orange Upper for {self.window}: {highest_hsv}\n')
                self.orange_lower = lowest_hsv
                self.orage_upper = highest_hsv
                break

            if cv2.waitKey(1) & 0xFF == ord('r'):
                # Make the limits revert back
                print(f'--> Limits Reset!')
                lowest_hsv = hsv_limits[0] 
                highest_hsv = hsv_limits[1]

            if cv2.waitKey(1) & 0xFF == ord('q'):
                # Exit
                self.release_camera()
                exit()

        # Release the VideoCapture and close all windows
        cv2.destroyAllWindows()
        pass

    def color_calibration(self):
        # TODO: Check if ranges are present in the references folder. Use those ranges or create new ones using get_hsv_ranges.
        self.get_hsv_ranges()


    def camera_calibration(self):
        # TODO: Aiden -> implement camera calibration and store in new object
        # Since this should only need to be completed one time per camera. Have the output saved as a .npy file with designation CAM1 and CAM2. 
        # We will need to put a label on the cameras as different computers use different paths to the webcams (Unless someone can figure this out. Look into how CV uses indecies as an input to VideoStream function).
        # Deciding which camera gets what matrix will happen by seeing what camera index gets used for the different cams and applying the correction Matricies to that camera.
        # See video for more information: https://www.youtube.com/watch?v=uKDAVcSaNZA
        ################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

        chessboardSize = (8,5)
        frameSize = (640,480)



        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
        objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)


        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpointsL = [] # 2d points in image plane.
        imgpointsR = [] # 2d points in image plane.


        imagesLeft = glob.glob('images/stereoLeft/*.png')
        imagesRight = glob.glob('images/stereoRight/*.png')

        for imgLeft, imgRight in zip(imagesLeft, imagesRight):

            imgL = cv2.imread(imgLeft)
            imgR = cv2.imread(imgRight)
            grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
            grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            retL, cornersL = cv2.findChessboardCorners(grayL, chessboardSize, None)
            retR, cornersR = cv2.findChessboardCorners(grayR, chessboardSize, None)

            # If found, add object points, image points (after refining them)
            if retL and retR == True:

                objpoints.append(objp)

                cornersL = cv2.cornerSubPix(grayL, cornersL, (11,11), (-1,-1), criteria)
                imgpointsL.append(cornersL)

                cornersR = cv2.cornerSubPix(grayR, cornersR, (11,11), (-1,-1), criteria)
                imgpointsR.append(cornersR)

                # Draw and display the corners
                cv2.drawChessboardCorners(imgL, chessboardSize, cornersL, retL)
                cv2.imshow('img left', imgL)
                cv2.drawChessboardCorners(imgR, chessboardSize, cornersR, retR)
                cv2.imshow('img right', imgR)
                cv2.waitKey(1000)


        cv2.destroyAllWindows()




        ############## CALIBRATION #######################################################

        retL, cameraMatrixL, distL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints, imgpointsL, frameSize, None, None)
        heightL, widthL, channelsL = imgL.shape
        newCameraMatrixL, roi_L = cv2.getOptimalNewCameraMatrix(cameraMatrixL, distL, (widthL, heightL), 1, (widthL, heightL))

        retR, cameraMatrixR, distR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints, imgpointsR, frameSize, None, None)
        heightR, widthR, channelsR = imgR.shape
        newCameraMatrixR, roi_R = cv2.getOptimalNewCameraMatrix(cameraMatrixR, distR, (widthR, heightR), 1, (widthR, heightR))



        ########## Stereo Vision Calibration #############################################

        flags = 0
        flags |= cv2.CALIB_FIX_INTRINSIC
        # Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
        # Hence intrinsic parameters are the same 

        criteria_stereo= (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
        retStereo, newCameraMatrixL, distL, newCameraMatrixR, distR, rot, trans, essentialMatrix, fundamentalMatrix = cv2.stereoCalibrate(objpoints, imgpointsL, imgpointsR, newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], criteria_stereo, flags)

        #print(newCameraMatrixL)
        #print(newCameraMatrixR)

        ########## Stereo Rectification #################################################

        rectifyScale= 1
        rectL, rectR, projMatrixL, projMatrixR, Q, roi_L, roi_R= cv2.stereoRectify(newCameraMatrixL, distL, newCameraMatrixR, distR, grayL.shape[::-1], rot, trans, rectifyScale,(0,0))

        stereoMapL = cv2.initUndistortRectifyMap(newCameraMatrixL, distL, rectL, projMatrixL, grayL.shape[::-1], cv2.CV_16SC2)
        stereoMapR = cv2.initUndistortRectifyMap(newCameraMatrixR, distR, rectR, projMatrixR, grayR.shape[::-1], cv2.CV_16SC2)

        print("Saving parameters!")
        cv_file = cv2.FileStorage('stereoMap.xml', cv2.FILE_STORAGE_WRITE)

        cv_file.write('stereoMapL_x',stereoMapL[0])
        cv_file.write('stereoMapL_y',stereoMapL[1])
        cv_file.write('stereoMapR_x',stereoMapR[0])
        cv_file.write('stereoMapR_y',stereoMapR[1])

        cv_file.release()


        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)    
        objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
        objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

        size_of_chessboard_squares_mm = 20
        objp = objp * size_of_chessboard_squares_mm


        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.


        images = glob.glob('images/*.png')


        for image in images:

            img = cv2.imread(image)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCornersSB(gray, chessboardSize, flags=cv2.CALIB_CB_EXHAUSTIVE)
            
            # If found, add object points, image points (after refining them)
            if ret == True:

                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
                imgpoints.append(corners)

                # Draw and display the corners
                cv2.drawChessboardCorners(img, chessboardSize, corners2, ret)
                cv2.imshow('img', img)
                cv2.waitKey(1000)


        cv2.destroyAllWindows()




        ############## CALIBRATION #######################################################

        ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

        # Save the camera calibration result for later use (we won't worry about rvecs / tvecs)
        pickle.dump((cameraMatrix, dist), open( "calibration.pkl", "wb" ))
        pickle.dump(cameraMatrix, open( "cameraMatrix.pkl", "wb" ))
        pickle.dump(dist, open( "dist.pkl", "wb" ))


        # ############## UNDISTORTION #####################################################
        count = 1
        for image in images:
            img = cv2.imread(image)
            h,  w = img.shape[:2]
            newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))



            # Undistort
            dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

            # crop the image
            x, y, w, h = roi
            dst = dst[y:y+h, x:x+w]
            cv2.imwrite(f'res_image{count}.png', dst)


            # Undistort with Remapping
            mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
            dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

            # crop the image
            x, y, w, h = roi
            dst = dst[y:y+h, x:x+w]
            cv2.imwrite(f'res_image{count}2.png', dst)
            count += 1




        # Reprojection Error
        mean_error = 0

        for i in range(len(objpoints)):
            imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
            error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
            mean_error += error

        print( "total error: {}".format(mean_error/len(objpoints)) )


        pass
    
    def hsv_mask_detec(self):
        # Inputs a frame from self
        # Outputs coordinates of the ball with radius in the form:  (x,y,r) 
        # Use code from previous method : found in colordetec.py
        if self.frame.all == None:
            return (None,None), None
        # Convert rgb to hsv space
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

        # Create mask for given color range
        mask = cv2.inRange(hsv,self.orange_lower,self.orange_upper)

        # find contours in the mask and initialize the current
		# (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        print(cnts)
        cnts = imutils.grab_contours(cnts)
        center = None
		# only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            (self.x,self.y), self.R = cv2.minEnclosingCircle(c)

    def binary_centroid(self):
        # Take masked frame and use a binary thresholding function to create a binary image. (Reduces the image from NxNx3 to NxN)./
        #   Then compute the centroid based on the values. Should output the x, y position in the frame.
        # TODO: Complete time testing vs the hsv_mask_detec function
        # I would expect this function to be faster than finding the contours with an opencv function.
        
        # Code borrowed from hsv_mask_detec to get the mask
        if not self.frame.all:
            self.x, self.y = None, None
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.orange_lower, self.orange_upper)

        # Compute the binary threshold of the mask
        ret, thresh = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        # If the threshold function fails, return early
        if not ret:
            self.x, self.y = None, None
            return
        
        # Calculate the indices of the coordinates where the frame is set to 1
        y_coords, x_coords = np.where(thresh)

        # Put them into a numpy array
        positions = np.array([np.median(x_coords), np.median(y_coords)])

        # If there are no pixels that are set to 1, then return early
        if np.any(np.isnan(positions)):
            self.x, self.y = None, None
            return
        # Finally, set self.x and self.y to the computed positions
        self.x, self.y = positions[0], positions[1]
        # Function doesn't detect radius; can change to whatever
        self.R = 10

        # TODO: implement background subtraction to only detect moving objects

    
        

    def run(self):
        # TODO: Eventually include multithreading with this function.  Will need to have the while loop included
        t0 = time.time()
        with gf:
            self.get_frame()
        gf_times.append(gf.took)
        # self.hsv_mask_detec()
        with bc:
            self.binary_centroid()
        bc_times.append(bc.took)
        with sf:    
            self.show_frame()
        sf_times.append(sf.took)
        self.fps = 1/(time.time() - t0)

    def release_camera(self):
        self.cap.release()
        print(f'{self.window} released!')

def ray_backtracking(Cam1, Cam2):
    with ray_timer:
        cam_matrix = np.array([[506.84856584,   0,         319.76019864],
                                [0,         506.82585053,  238.71317098],
                                [0,           0,           1,        ]]) # hard coded from camera calibration
        if not (Cam1.x and Cam1.y and Cam2.x and Cam2.y):
            return
        Ki_1 = np.linalg.inv(cam_matrix)
        ray1 = Ki_1.dot([Cam1.x, Cam1.y, 1.0])
        Ki_2 = np.linalg.inv(cam_matrix)
        ray2 = Ki_2.dot([Cam2.x, Cam2.y, 1.0])
        
        cos_angle = ray1.dot(ray2) / (np.linalg.norm(ray1) * np.linalg.norm(ray2))
        angle_radians = np.arccos(cos_angle)
        angle_degrees = angle_radians * 180 / 3.141592
    ray_times.append(ray_timer.took)
    #print(angle_radians)
    #print(angle_degrees)

    

# Test code 
Cam1 = Cam(camID = 1)
Cam2 = Cam(camID = 2)
# try:
#     Cam1.find_camera_id()
# except:
#     Cam1.release_camera()
Cam1.set_camera_id()

Cam1.color_calibration()

# try:
#     Cam2.find_camera_id()
# except:
#     Cam2.release_camera()
Cam2.set_camera_id()

Cam2.color_calibration()
gf_times, bc_times, sf_times,ray_times, loop_times = [], [], [], [], []
gf = CodeTimer("Get Frame", silent=True)
bc = CodeTimer("Binary Centroid", silent=True)
sf = CodeTimer("Show Frame", silent=True)
ray_timer = CodeTimer("Ray Timer", silent = True)
loop_timer = CodeTimer("Loop Timer", silent = True)
print("Press q to release cameras and exit.\n")
while True:
    with loop_timer:
        Cam1.run()
        Cam2.run()
        
        ray_timer = CodeTimer()
        ray_backtracking(Cam1, Cam2) 
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            Cam1.release_camera()
            Cam2.release_camera()
            break
    loop_times.append(loop_timer.took)
        
cv2.destroyAllWindows()
print(f"The average time taken to fully loop was {round(np.average(loop_times[3:-3]), 5)} ms")
print(f"The average time taken to get frame was {round(np.average(gf_times[3:-3]), 5)} ms")
print(f"The average time taken to do binary centroid was {round(np.average(bc_times[3:-3]), 5)} ms")
print(f"The average time taken to show frame was {round(np.average(sf_times[3:-3]), 5)} ms")
print(f"The average time taken to calculate rays was {round(np.average(ray_times[3:-3]), 5)} ms")