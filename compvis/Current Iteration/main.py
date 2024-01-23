import cv2
import time
import numpy as np
from camera import camera_instantiator
from timers import timers
from triangulation import LSLocalizer
from predict import RLS
import matplotlib.pyplot as plt


def calculate_points(lsl, rays, calculated_pts):
    ray_vals = np.array(list(rays.values()))
    calculated_pt = lsl.predict(ray_vals)
    calculated_pts.append(calculated_pt)
    print(f"Calculated point: {calculated_pt}")
    return calculated_pt


def fit_and_predict_rls(rls, calculated_pts):
    labels = [time.time()] * len(calculated_pts)
    rls.fit(calculated_pts, labels)
    calculated_pt = calculated_pts[-1]
    next_point = rls.predict(np.insert(calculated_pt, 0, 1))
    print(f"Predicted next point: {next_point}")


def draw_points(ax, new_point):
    x, y, z = new_point[0], new_point[1], new_point[2]
    ax.scatter(x, y, z, c="orange", marker="o", s=100)
    ax.plot(x, y, z, color="r")
    ax.set_xlabel("X"), ax.set_ylabel("Y"), ax.set_zlabel("Z")


def main_loop(cameras, lsl, rls):
    calculated_pts = []
    ax = plt.axes(projection="3d")

    while True:
        with timers.timers["Main Loop"]:
            if cv2.waitKey(1) == ord("q"):
                for camera in cameras.values():
                    camera.release_camera()
                break

            rays = {
                camera: camera.run()
                for camera in cameras.values()
                if camera.ball_located
            }

            if rays:
                calculated_point = calculate_points(lsl, rays, calculated_pts)
                if len(calculated_pts) % 30 == 0:
                    draw_points(ax, calculated_point)

            # fit_and_predict_rls(rls, calculated_pts)

        timers.record_time("Main Loop")
    plt.show()


def main(camera_transforms, cam_ids=None):
    cameras = camera_instantiator(cam_ids)
    print("Press q to release cameras and exit.\n")
    lam = 0.98
    rls = RLS(4, lam, 1)
    lsl = LSLocalizer(camera_transforms)
    main_loop(cameras, lsl, rls)

    cv2.destroyAllWindows()
    timers.display_averages()


if __name__ == "__main__":
    # first camera at origin
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
