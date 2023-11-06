"""Stereo_Vision.py
This module accepts the ball's position in pixel space and returns the ball's position in the base frame using triangle similarity.

@Author:                Vincent Rimparsurat
@Date:                  2023-11-06 16:06:30
@Last Modified by:      Vincent Rimparsurat
@Last Modified time:    2020-11-02 17:08:30
"""

class StereoVision():
    """Finds the ball's position in the base frame.
    
    Uses the method found at https://www.youtube.com/watch?v=uKDAVcSaNZA to find the distance between camera and the ball (z coordinate). Averages the positions found in the projected plane for the x and y coordinates.
    """

    def __init__(self, left_cam_transform, right_cam_transform):
        """Initialize the stereo vision localizer with the SE(3) transforms of both cameras, using inches for displacement, relative to the base frame.
        """
        pass

    def stereo_camera_calibration(self):
        """Calibrate the cameras to undistort the image.
        """
        pass

    def localize(self, left_pixel_coordinate, right_pixel_coordinate):
        """Find the coordinates of the ball in the base frame.
        """
        pass



    