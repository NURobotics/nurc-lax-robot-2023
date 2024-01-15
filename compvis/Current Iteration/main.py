import cv2, time
import numpy as np
from rays import ray_backtracking
from camera_identification import camera_instantiator
from camera_class import timers

def main(cam_ids):
    cameras = camera_instantiator(cam_ids)
    print("Press q to release cameras and exit.\n")
    
    while True:
        with timers.loop:
            for camera in cameras.values():
                camera.run()
                
            # Check if the correct number of cameras have been instantiated to use ray_backtracking, if so proceed
            camera_list = list(cameras.values())
            if len(camera_list) == 2:
                with timers.ray:
                    rays = ray_backtracking(camera_list[0], camera_list[1])
                    # TODO Implement triangulation based upon the rays returned
                timers.ray_times.append(timers.ray.took)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                for camera in cameras.values():
                    camera.release_camera()
                break

        timers.loop_times.append(timers.loop.took)

    cv2.destroyAllWindows()

    print(f"The average time taken to fully loop was {round(np.average(timers.loop_times), 5)} ms")
    print(f"The average time taken to get frame was {round(np.average(timers.gf_times), 5)} ms")
    print(f"The average time taken to do binary centroid was {round(np.average(timers.bc_times), 5)} ms")
    print(f"The average time taken to show frame was {round(np.average(timers.sf_times), 5)} ms")
    print(f"The average time taken to calculate rays was {round(np.average(timers.ray_times), 5)} ms" if timers.ray_times else "No rays calculated")

        
if __name__ == "__main__":
    main([0])
    
    
    
    
    
    
    
    
    
    
    
    
