import numpy as np


def ray_backtracking(cam1, cam2):
    """
    Perform ray backtracking based on camera calibration and image coordinates.

    Parameters:
    - cam1 (object): Object representing the first camera with attributes x and y (image coordinates).
    - cam2 (object): Object representing the second camera with attributes x and y (image coordinates).

    Returns:
    tuple: Tuple containing normalized unit vectors of ray directions for cam1 and cam2.
    """

    cam_matrix = np.array(
        [
            [506.84856584, 0, 319.76019864],
            [0, 506.82585053, 238.71317098],
            [0, 0, 1],
        ]
    )  # hard coded from camera calibration

    # Check if image coordinates are available for both cameras
    if not (cam1.x and cam1.y and cam2.x and cam2.y):
        pass

    # Calculate ray directions for cam1
    Ki_1 = np.linalg.inv(cam_matrix)
    ray1 = Ki_1.dot([cam1.x, cam1.y, 1.0])
    ray1_norm = np.linalg.norm(ray1)
    ray1_unit = ray1 / ray1_norm

    # Calculate ray directions for cam2
    Ki_2 = np.linalg.inv(cam_matrix)
    ray2 = Ki_2.dot([cam2.x, cam2.y, 1.0])
    ray2_norm = np.linalg.norm(ray2)
    ray2_unit = ray2 / ray2_norm

    print(f"ray 1 unit vec {ray1_unit}")
    print(f"ray 2 unit vec {ray2_unit}")

    return (ray1_unit, ray2_unit)

    # Additional code (commented out)
    # cos_angle = ray1.dot(ray2) / (np.linalg.norm(ray1) * np.linalg.norm(ray2))
    # angle_radians = np.arccos(cos_angle)
    # angle_degrees = angle_radians * 180 / 3.141592
