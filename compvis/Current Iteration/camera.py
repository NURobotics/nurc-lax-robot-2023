import cv2
import time
import numpy as np
from linetimer import CodeTimer
from masks import binary_centroid, get_hsv_ranges
from frames import get_frame, show_frame
from rays import ray_backtracking


class Timers:
    """
    Timer class to measure execution times of various functions.
    """

    def __init__(self):
        self.gf = CodeTimer("Get Frame", silent=True)
        self.bc = CodeTimer("Binary Centroid", silent=True)
        self.sf = CodeTimer("Show Frame", silent=True)
        self.loop = CodeTimer("Loop Timer", silent=True)
        self.ray = CodeTimer("Ray Timer", silent=True)
        self.gf_times = []
        self.bc_times = []
        self.sf_times = []
        self.loop_times = []
        self.ray_times = []


timers = Timers()


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

    def print_ball_pos(self):
        """
        Print the position of the detected object (not used in code).
        """
        if self.x and self.y and self.R:
            print(self.x, self.y, self.R)

    def color_calibration(self):
        """
        Perform color calibration using HSV ranges (not used in code).
        """
        get_hsv_ranges(self)

    def release_camera(self):
        """
        Release the camera object.
        """
        self.cap.release()
        print(f"{self.window} released!")

    def run(self):
        """
        Run the camera processing loop.
        """
        t0 = time.time()
        with timers.gf:
            get_frame(self)
        timers.gf_times.append(timers.gf.took)

        with timers.bc:
            binary_centroid(self)
        timers.bc_times.append(timers.bc.took)

        with timers.sf:
            show_frame(self)
        timers.sf_times.append(timers.sf.took)

        self.fps = 1 / (time.time() - t0)
