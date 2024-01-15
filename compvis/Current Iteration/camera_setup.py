import cv2
import numpy as np
from masks import get_hsv_ranges
from camera_class import Cam

def find_camera_ids():
    # Loop over camera ID's and display their outputs to the user to make sure the you have the correct webcam. Make sure to know what camera is what
    # If you see the videostream you are looking for press s and the the camID will be saved to the class. If you want to move to the next id press q. 
    # TODO: Fix bug where if there is no camera 
    ids = []
    for cam_id in range(3):  # Adjust the range based on the number of cameras you want to check

        cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
        ret, frame = cap.read()
        if ret:
            ids.append(cam_id)
        
        
    return ids


    
def set_camera_id(Camera):
    cap = cv2.VideoCapture(Camera.camID, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"Camera ID {Camera.camID} is not available.")
    
    print("Press s to use displayed camera.\nPress q to skip to the next camera.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to retrieve frame from Camera ID {Camera.camID}.")
            break

        cv2.imshow(f"Camera ID {Camera.camID}", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
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
    if cam_ids is None: 
        cam_ids = find_camera_ids()
     
    for cam_id in cam_ids:
        cam_name = f"Cam{cam_id}"
        cameras[cam_name] = Cam(camID= cam_id)
        set_camera_id(cameras[cam_name])
            
    for camera in cameras.values():
        print(camera)
        get_hsv_ranges(camera)
        
    return cameras