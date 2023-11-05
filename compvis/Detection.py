import cv2
import imutils

class Detection():
    
    # Outputs: The 2D position of the ball in the pixel space
    
    def __init__(self, N):
        self.cap = cv2.VideoCapture(N)
        self.frame = None
        self.orangeUpper = (18, 255, 255)
        self.orangeLower = (10, 149, 138)

        

    def get_frame(self):
        # Outputs the frame from the cap object
        # Eventually include multithreading
        ret,frame = self.cap.read()
        if ret:
            self.frame = frame
        else:
            self.frame = None





    def color_calibration(self):
        # Complete color calibration for each camera to get the proper range of hsv values for the environment

        #self.orangeUpper = ...
        #self.orangeLower = ...
        pass
            

        

    def color_mask_circle_detec(self):
        # Inputs a frame from self
        # Outputs coordinates of the ball with radius in the form:  (x,y,r) 
        # Use code from previous method : found in colordetec.py
        if self.frame.all == None:
            return (None,None), None
        # Convert rgb to hsv space
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

        # Create mask for given color range
        mask = cv2.inRange(hsv,self.orangeLower,self.orangeUpper)

        # find contours in the mask and initialize the current
		# (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
		# only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            return cv2.minEnclosingCircle(c)

        

    
    def release_camera(self):
        self.cap.release()
        


# Test code 
Cam1 = Detection(0)
cv2.namedWindow('Video Stream')
while(1):
    Cam1.get_frame()
    if Cam1.frame.all != None:
        (x,y),R = Cam1.color_mask_circle_detec()

    cv2.imshow("Video Stream", Cam1.frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        Cam1.release_camera()
        break
cv2.destroyAllWindows()


