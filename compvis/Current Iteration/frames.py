import cv2


def get_frame(camera):
    """
    Update the camera's frame.

    Parameters:
    - camera (Cam): Camera object.

    Returns:
    None
    """
    ret, frame = camera.cap.read()
    if ret:
        camera.frame = frame
    else:
        camera.frame = None


def show_frame(camera):
    """
    Display the camera's frame with optional circle and fps information.

    Parameters:
    - camera (Cam): Camera object.

    Returns:
    None
    """
    if camera.x and camera.y and camera.R:
        cv2.circle(
            camera.frame,
            (int(camera.x), int(camera.y)),
            int(camera.R),
            (0, 255, 255),
            2,
        )

    if camera.fps:
        cv2.putText(
            camera.frame, str(camera.fps), (camera.W - 100, 50), 0, 1, (0, 255, 0), 2
        )

    cv2.imshow(camera.window, camera.frame)
