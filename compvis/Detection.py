import cv2

class Detection():
    
    # Outputs: The 2D position of the ball in the pixel space
    
    def __init__(self, N):
        self.cap = cv2.VideoCapture(N)
        self.frame = None
        self.orangeUpper = None
        self.orangeLower = None

        

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
        # Convert rgb to hsv space


        # Outputs coordinates of the ball with radius in the form:  (x,y,r) 
        # Use code from previous method : found in colordetec.py

        pass

    
    def release_camera(self):
        self.cap.release()
        


# Test code 
Cam1 = Detection(0)
cv2.namedWindow('Video Stream')
while(1):
    Cam1.get_frame()
    cv2.imshow("Video Stream", Cam1.frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        Cam1.release_camera()
        break
cv2.destroyAllWindows()


