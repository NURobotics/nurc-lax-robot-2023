import cv2
import imutils
import time
import numpy as np


class Cam():
    # Class to initialize webcams and output the position of the ball in the frame. 
    # Begin by initializing the class with no inputs.
    # Use find_camera_id to get the find the correct webcam


    def __init__(self):
        self.cap = None
        self.frame = None
        self.hsv_value = None
        self.orange_upper = np.array([18, 255, 255])
        self.orange_lower = np.array([10, 149, 138])
        self.window = None
        self.camID = None
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




        for cam_id in range(5):  # Adjust the range based on the number of cameras you want to check
            cap = cv2.VideoCapture(cam_id)
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
        cnts = imutils.grab_contours(cnts)
        center = None
		# only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            (self.x,self.y), self.R = cv2.minEnclosingCircle(c)

    def binary_centroid():
        # TODO: Take masked frame and use a binary thresholding function to create a binary image. (Reduces the image from NxNx3 to NxN)./
        #   Then compute the centroid based on the values. Should output the x, y position in the frame.
        # TODO: Complete time testing vs the hsv_mask_detec function
        # I would expect this function to be faster than finding the contours with an opencv function.
        pass

    def run(self):
        # TODO: Eventually include multithreading with this function.  Will need to have the while loop included
        t0 = time.time()
        self.get_frame()
        self.hsv_mask_detec()
        self.show_frame()
        self.fps = 1/(time.time() - t0)

    def release_camera(self):
        self.cap.release()
        print(f'{self.window} released!')

    

# Test code 
Cam1 = Cam()
Cam2 = Cam()
try:
    Cam1.find_camera_id()
except:
    Cam1.release_camera()


Cam1.color_calibration()

try:
    Cam2.find_camera_id()
except:
    Cam2.release_camera()

Cam2.color_calibration()

print("Press q to release cameras and exit.\n")
while(1):
    Cam1.run()
    Cam2.run()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        Cam1.release_camera()
        Cam2.release_camera()
        break
cv2.destroyAllWindows()


