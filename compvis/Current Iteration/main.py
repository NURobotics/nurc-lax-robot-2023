import cv2, time
import numpy as np
from camera import camera_instantiator
from timers import timers
from triangulation import LSLocalizer

""" 
Cam_ids is an array with which the user specifies which cameras are to be used... 
eg: cam_ids = [0] uses laptop webcam -- cam_ids = [1,2] uses 2 external cameras
If given none it will default to finding the cam_ids function
"""


def main(camera_transforms, cam_ids=None):
    cameras = camera_instantiator(cam_ids)
    print("Press q to release cameras and exit.\n")

    while True:
        with timers.timers["Loop Timer"]:
            if cv2.waitKey(1) & 0xFF == ord("q"):
                for camera in cameras.values():
                    camera.release_camera()
                break
            
            rays = {camera: camera.run() for camera in cameras.values() if camera.ball_located}
                    
            if rays:
                #TODO need to correctly implement camera transforms in main
                lsl = LSLocalizer(camera_transforms)
                predicted_point = lsl.predict(rays.values())
                print(f"Predicted point: {predicted_point}")

        timers.record_time("Loop Timer")

    cv2.destroyAllWindows()
    timers.display_averages()



if __name__ == "__main__":
    T_cam1 = np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )

    # second camera rotated pi/2 about Z at (1, 1, 0)
    T_cam2 = np.array(
        [
            [0, -1, 0, 1],
            [1, 0, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    camera_transforms = [T_cam1, T_cam2]
    main(camera_transforms)
