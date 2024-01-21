import cv2, time
import numpy as np
from camera import timers, camera_instantiator
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
        with timers.loop:
            rays = {} # dict to make debugging easier
            for camera in cameras.values():
                camera.run()
                if camera.located():
                    rays[camera] = camera.get_ray()
            
            if len(rays.values()) != 2:
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    for camera in cameras.values():
                        camera.release_camera()
                    break
                continue 
                
            with timers.ray:
                #TODO need to correctly implement camera transforms in main
                lsl = LSLocalizer(camera_transforms)
                predicted_point = lsl.predict(rays.values())
                print(f"Predicted point: {predicted_point}")
            timers.ray_times.append(timers.ray.took)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                for camera in cameras.values():
                    camera.release_camera()
                break

        timers.loop_times.append(timers.loop.took)

    cv2.destroyAllWindows()

    print(
        f"The average time taken to fully loop was {round(np.average(timers.loop_times), 5)} ms"
    )
    print(
        f"The average time taken to get frame was {round(np.average(timers.gf_times), 5)} ms"
    )
    print(
        f"The average time taken to do binary centroid was {round(np.average(timers.bc_times), 5)} ms"
    )
    print(
        f"The average time taken to show frame was {round(np.average(timers.sf_times), 5)} ms"
    )
    print(
        f"The average time taken to calculate rays was {round(np.average(timers.ray_times), 5)} ms"
        if timers.ray_times
        else "No rays calculated"
    )


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
    main(camera_transforms, [0])
