import cv2

class Detection():
    
    # Outputs: The 2D position of the ball in the pixel space

    def __init__(self) -> None:
        pass

    def initialize_cam(N):
        # N specifies the camera number 0 for mac webcam, typically 1 for mac webcam
        # Initialize a camera video stream
        # Eventually include multithreading
        cap = cv2.VideoCapture(N)

        return cap

    def color_calibration(cap):
        # Complete color calibration for each camera to get the proper range of hsv values for the environment
        while(1):
            ret, frame = cap.read()
            if not ret :
                print("Error: Could not read frame")
                break

            # Create a window to display the video stream
            cv2.namedWindow('Video Stream')
            cv2.setMouseCallback('Video Stream', get_hsv_range)
            

        

    def color_mask_circle_detec():
        # Use code from previous method : found in colordetec.py
        pass