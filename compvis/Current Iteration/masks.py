import cv2
import numpy as np
from frames import get_frame
""" 
1/14/24 Need to fix resetting mask -- current implementation does not support

"""

def binary_centroid(Camera):
    # Take masked frame and use a binary thresholding function to create a binary image. (Reduces the image from NxNx3 to NxN)./
    #   Then compute the centroid based on the values. Should output the x, y position in the frame.
    # TODO: Complete time testing vs the hsv_mask_detec function
    # I would expect this function to be faster than finding the contours with an opencv function.
    
    # Code borrowed from hsv_mask_detec to get the mask
    if not Camera.frame.all:
        Camera.x, Camera.y = None, None
    hsv = cv2.cvtColor(Camera.frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, Camera.orange_lower, Camera.orange_upper)

    # Compute the binary threshold of the mask
    ret, thresh = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
    # If the threshold function fails, return early
    if not ret:
        Camera.x, Camera.y = None, None
        return 
    
    # Calculate the indices of the coordinates where the frame is set to 1
    y_coords, x_coords = np.where(thresh)

    # Put them into a numpy array
    positions = np.array([np.median(x_coords), np.median(y_coords)])

    # If there are no pixels that are set to 1, then return early
    if np.any(np.isnan(positions)):
        Camera.x, Camera.y = None, None
        return 
    # Finally, set Camera.x and Camera.y to the computed positions
    Camera.x, Camera.y = positions[0], positions[1]
    # Function doesn't detect radius; can change to whatever
    Camera.R = 10
    
    
def get_hsv_ranges(Camera):
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

                
                Camera.hsv_value = lower_hsv, upper_hsv
        
        hsv_values = []

        highest_hsv = np.array([0, 0, 0])
        lowest_hsv = np.array([180, 255, 255])
        hsv_limits = [lowest_hsv, highest_hsv]
        cv2.namedWindow('Video Stream')
        cv2.setMouseCallback('Video Stream', get_hsv_range)
        print("Click on the Video Stream frame until the mask looks correct.\nPress s to save hsv bounds.\nPress r to reset mask.\nPress q to exit")
        while True:
            get_frame(Camera)
             # Convert the frame to the HSV color space
            hsv_frame = cv2.cvtColor(Camera.frame, cv2.COLOR_BGR2HSV)


            if Camera.hsv_value:

                if np.any(np.isin(Camera.hsv_value, hsv_values, invert=True)): # inserts a new hsv_value into the array if it is not already in the array
                    hsv_values.append(Camera.hsv_value) 
                
                lowest_hsv = np.array([min(lowest_hsv[0], Camera.hsv_value[0][0]),min(lowest_hsv[1], Camera.hsv_value[0][1]), min(lowest_hsv[2], Camera.hsv_value[0][2])])
                highest_hsv = np.array([max(highest_hsv[0], Camera.hsv_value[1][0]),max(highest_hsv[1], Camera.hsv_value[1][1]), max(highest_hsv[2], Camera.hsv_value[1][2])])
                    
                mask = cv2.inRange(hsv_frame, lowest_hsv, highest_hsv)
                #result = cv2.bitwise_and(Camera.frame, Camera.frame, mask=mask)
                mask_inv = cv2.bitwise_not(mask)
                result = cv2.bitwise_and(Camera.frame,Camera.frame, mask=mask_inv)
                cv2.imshow('Video Stream', result)
                
            if Camera.hsv_value is None:
                cv2.imshow('Video Stream', Camera.frame)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                print(f'--> Orange Lower for {Camera.window}: {lowest_hsv}')
                print(f'--> Orange Upper for {Camera.window}: {highest_hsv}\n')
                Camera.orange_lower = lowest_hsv
                Camera.orage_upper = highest_hsv
                break

            if cv2.waitKey(1) & 0xFF == ord('r'):
                # Make the limits revert back
                print(f'--> Limits Reset!')
                lowest_hsv = np.array([180, 255, 255])
                highest_hsv = np.array([0, 0, 0])
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # Exit
                Camera.release_camera()
                exit()

        # Release the VideoCapture and close all windows
        cv2.destroyAllWindows()
        pass
    
    
    
# I believe that this is unused legacy code but it falls into this bin
#
# def hsv_mask_detec(self):
#         # Inputs a frame from self
#         # Outputs coordinates of the ball with radius in the form:  (x,y,r) 
#         # Use code from previous method : found in colordetec.py
#         if self.frame.all == None:
#             return (None,None), None
#         # Convert rgb to hsv space
#         hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

#         # Create mask for given color range
#         mask = cv2.inRange(hsv,self.orange_lower,self.orange_upper)

#         # find contours in the mask and initialize the current
# 		# (x, y) center of the ball
#         cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         print(cnts)
#         cnts = imutils.grab_contours(cnts)
#         center = None
# 		# only proceed if at least one contour was found
#         if len(cnts) > 0:
#             # find the largest contour in the mask, then use
#             # it to compute the minimum enclosing circle and
#             # centroid
#             c = max(cnts, key=cv2.contourArea)
#             (self.x,self.y), self.R = cv2.minEnclosingCircle(c)
