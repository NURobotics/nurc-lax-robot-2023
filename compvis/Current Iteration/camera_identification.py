import cv2
import numpy as np
from masks import get_hsv_ranges
from camera_class import Cam

def find_camera_id(Camera):
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
                Camera.camID = cam_id
                Camera.cap = cap
                Camera.window = (f'Cam {Camera.camID}')
                Camera.H = np.shape(frame)[0]
                Camera.W = np.shape(frame)[1]
                print(f'--> Camera Index: [{Camera.camID}] saved!\n')
                cv2.destroyAllWindows()
                return
                
            if key == ord('q'):
                print("--> Camera skipped!")
                break
            


        cap.release()
        cv2.destroyAllWindows()
    
    pass

    
def set_camera_id(Camera):
    cam_id = Camera.camID
    cap = cv2.VideoCapture(Camera.camID, cv2.CAP_DSHOW)
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
            Camera.camID = cam_id
            Camera.cap = cap
            Camera.window = (f'Cam {Camera.camID}')
            Camera.H = np.shape(frame)[0]
            Camera.W = np.shape(frame)[1]
            print(f'--> Camera Index: [{Camera.camID}] saved!\n')
            cv2.destroyAllWindows()
            return
            
        if key == ord('q'):
            print("--> Camera skipped!")
            break
        


    cap.release()
    cv2.destroyAllWindows()
    
    pass

def camera_instantiator(cam_ids):
    # quick function to set up each camera 
    cameras = {}
    for cam_id in cam_ids:
        cam_name = f"Cam{cam_id}"
        cameras[cam_name] = Cam(cam_id)
        set_camera_id(cameras[cam_name])
        get_hsv_ranges(cameras[cam_name])
    return cameras