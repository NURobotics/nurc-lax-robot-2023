import cv2
import imutils
import threading

class Cam():
    # Inputs the Videocamera number to be used in cv2.VideoCapture()
    def __init__(self,N):
        self.cap = cv2.VideoCapture(N)
        self.frame = None
        self.orange_upper = (18, 255, 255)
        self.orange_lower = (10, 149, 138)
        self.window = (f'Cam {N}')
        self.x = None 
        self.y = None
        self.R = None
    
    def get_frame(self):
        # Outputs the frame from the cap object
        # Eventually include multithreading
        ret,frame = self.cap.read()
        if ret:
            self.frame = frame
        else:
            self.frame = None

    def show_frame(self):
        if self.x and self.y and self.R != None:
            cv2.circle(self.frame, (int(self.x), int(self.y)), int(self.R), (0, 255, 255), 2)

        cv2.imshow(self.window,self.frame)

    def print_ball_pos(self):
        if self.x and self.y and self.R != None:
            print(self.x, self.y, self.R)

    def color_calibration(self):
        # Complete color calibration for each camera to get the proper range of hsv values for the environment

        #self.orangeUpper = ...
        #self.orangeLower = ...
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
            (self.x,self.y), self.R = cv2.minEnclosingCircle(c)

    def run(self):
        self.get_frame()
        self.hsv_mask_detec()
        self.show_frame()


    def release_camera(self):
        self.cap.release()

    

# Test code 
Detec1 = Cam(0)

while(1):
    Detec1.run()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        Detec1.release_camera()
        break
cv2.destroyAllWindows()


