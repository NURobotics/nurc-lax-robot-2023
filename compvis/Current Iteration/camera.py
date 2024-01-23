import cv2 as cv
import time
import numpy as np
from masks import binary_centroid, get_hsv_ranges
from timers import timers


class Cam:
    """
    Camera class representing a video camera.

    Attributes:
    - cap: VideoCapture object for camera.
    - frame: Current frame from the camera.
    - hsv_value: HSV value range for color detection.
    - orange_upper: Upper HSV range for orange color.
    - orange_lower: Lower HSV range for orange color.
    - window: Name of the camera window.
    - camID: Camera ID.
    - x: X-coordinate of detected object.
    - y: Y-coordinate of detected object.
    - R: Radius of detected object.
    - fps: Frames per second.
    - W: Width of the frame in pixels.
    - H: Height of the frame in pixels.
    """

    def __init__(self, camID=None):
        self.cap = None
        self.frame = None
        self.hsv_value = None
        self.orange_upper = np.array([18, 255, 255])
        self.orange_lower = np.array([10, 149, 138])
        self.window = None
        self.camID = camID
        self.x = None
        self.y = None
        self.R = None
        self.fps = None
        # Height and Width of the frame in pixels
        self.W = None
        self.H = None
        self.cam_matrix = np.array(
            [[500, 0, 320], [0, 500, 240], [0, 0, 1]]
        )  # hard coded from camera calibration

    def release_camera(self):
        self.cap.release()
        print(f"{self.window} released!")

    def set_id(self, id):
        self.camID = id
        return id

    def get_id(self):
        return self.camID

    def has_id(self):
        return not self.camID == -1

    def get_cap(self):
        return self.cap

    def set_cap(self, cap):
        self.cap = cap

    def get_frame(self):
        _, frame = self.cap.read()
        self.frame = frame
        return frame

    def ball_located(self):
        return self.x and self.y

    def show_circled_frame(self):
        if self.x and self.y and self.R:
            cv.circle(
                self.frame,
                (int(self.x), int(self.y)),
                int(self.R),
                (0, 255, 255),
                2,
            )

        if self.fps:
            cv.putText(
                self.frame, str(self.fps), (self.W - 100, 50), 0, 1, (0, 255, 0), 2
            )

        cv.imshow(self.window, self.frame)

    def get_ray(self):
        if not (self.x and self.y):
            pass
        Ki = np.linalg.inv(self.cam_matrix)
        ray = Ki @ np.array([self.x, self.y, 1.0])
        ray_norm = ray / np.linalg.norm(ray)

        # cos_angle = ray1.dot(ray2) / (np.linalg.norm(ray1) * np.linalg.norm(ray2))
        # angle_radians = np.arccos(cos_angle)
        # angle_degrees = angle_radians * 180 / 3.141592
        return np.array([ray_norm[0], ray_norm[2], -ray_norm[1]])  # unit vector

    def set_camera_id(self):
        cap = cv.VideoCapture(self.camID, cv.CAP_DSHOW)
        if not cap.isOpened():
            print(f"camera ID {self.camID} is not available.")

        print("Press s to use displayed camera.\nPress q to skip to the next camera.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"Failed to retrieve frame from camera ID {self.camID}.")
                break

            cv.imshow(f"camera ID {self.camID}", frame)
            key = cv.waitKey(1)
            if key == ord("s"):
                self.cap = cap
                self.window = f"Cam {self.camID}"
                self.H = np.shape(frame)[0]
                self.W = np.shape(frame)[1]
                print(f"--> camera Index: [{self.camID}] saved!\n")
                cv.destroyAllWindows()
                return

            if key == ord("q"):
                print("--> camera skipped!")
                break

        cap.release()
        cv.destroyAllWindows()

    def run(self):
        t0 = time.time()
        with timers.timers["Get Frame"]:
            self.get_frame()
        timers.record_time("Get Frame")

        with timers.timers["Binary Centroid"]:
            binary_centroid(self)
        timers.record_time("Binary Centroid")

        with timers.timers["Show Frame"]:
            self.show_circled_frame()
        timers.record_time("Show Frame")

        self.fps = 1 / (time.time() - t0)

        return self.get_ray()


def find_camera_ids():
    ids = []
    for cam_id in range(
        3
    ):  # Adjust the range based on the number of cameras you want to check
        cap = cv.VideoCapture(cam_id, cv.CAP_DSHOW)
        ret, _ = cap.read()
        if ret:
            ids.append(cam_id)
    return ids


def camera_instantiator(cam_ids=None):
    # quick function to set up each camera
    cameras = {}
    if cam_ids is None:
        cam_ids = find_camera_ids()

    for cam_id in cam_ids:
        cam_name = f"Cam{cam_id}"

        # cap = None fix
        test_cam = Cam(camID=cam_id)
        test_cam.set_camera_id()

        if test_cam.cap:
            cameras[cam_name] = test_cam

    for camera in cameras.values():
        get_hsv_ranges(camera)

    return cameras


if __name__ == "__main__":
    cameras = camera_instantiator()
    verbose = True
    while True:
        for camera in cameras.values():
            if verbose:
                print(
                    f"Does Cam{camera.get_id()} currently have a set id? {camera.has_id()}"
                )
                verbose = False
            camera.run()
        if cv.waitKey(1) == ord("q"):
            for camera in cameras.values():
                camera.release_camera()
            break
