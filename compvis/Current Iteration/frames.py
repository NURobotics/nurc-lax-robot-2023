import cv2


def get_frame(Camera):
    # Outputs the frame from the cap object
    ret,frame = Camera.cap.read()
    if ret:
        Camera.frame = frame
    else:
        Camera.frame = None

def show_frame(Camera):
    if Camera.x and Camera.y and Camera.R:
        cv2.circle(Camera.frame, (int(Camera.x), int(Camera.y)), int(Camera.R), (0, 255, 255), 2)

    if Camera.fps:
        cv2.putText(Camera.frame, str(Camera.fps), (Camera.W - 100, 50), 0, 1, (0, 255, 0), 2)

    cv2.imshow(Camera.window,Camera.frame)