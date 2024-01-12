# import numpy as np
# import cv2 as cv

# arr = None
# window = "Multiple camera test"
# cv.namedWindow(window)


# while True:
#     for i in range(1):
#         cap = cv.VideoCapture(i)
#         ret, frame = cap.read()

#         if arr is None:
#             arr = frame
#         else:
#             arr = np.hstack((arr, frame))
        
#     cv.imshow(window, arr)
#     arr = None

#     if cv.waitKey(1) == ord("q"):
#         break


# window1 = "Cam 1"
# window2 = "Cam 2"
# cap1 = cv.VideoCapture(0)
# cap2 = cv.VideoCapture(2)
# cv.namedWindow(window1)
# cv.namedWindow(window2)

# while True:
#     ret, frame1 = cap1.read()
#     ret, frame2 = cap2.read()

#     if not ret:
#         print("From not received successfully")
#         break


#     # frame = np.hstack((frame1, frame2))
#     # cv.imshow(window1, frame1)
#     # cv.imshow(window2, frame2)
#     if cv.waitKey(1) == ord("q"):
#         break

# cap1.release()
# cap2.release()
# cv.destroyAllWindows()

# from threading import Thread
# import cv2, time
 
# class VideoStreamWidget(object):
#     def __init__(self, src=0):
#         self.src = src
#         self.capture = cv2.VideoCapture(src)
#         # Start the thread to read frames from the video stream
#         self.thread = Thread(target=self.update, args=())
#         self.thread.daemon = True
#         self.thread.start()

#     def update(self):
#         # Read the next frame from the stream in a different thread
#         while True:
#             if self.capture.isOpened():
#                 (self.status, self.frame) = self.capture.read()
#             time.sleep(.01)
    
#     def show_frame(self):
#         # Display frames in main program
#         cv2.imshow(f"frame-{self.src}", self.frame)
#         key = cv2.waitKey(1)
#         if key == ord('q'):
#             self.capture.release()
#             cv2.destroyAllWindows()
#             exit(1)

# if __name__ == '__main__':
#     stream_0 = VideoStreamWidget(0)
#     stream_1 = VideoStreamWidget(1)
#     stream_2 = VideoStreamWidget(2)
#     while True:
#         try:
#             # stream_0.show_frame()
#             pass
#         except AttributeError:
#             pass
#         try:
#             # stream_1.show_frame()
#             pass
#         except AttributeError:
#             pass
#         try:
#             stream_2.show_frame()
#         except AttributeError:
#             pass

import numpy as np
import cv2

captures = [
    cv2.VideoCapture(0, cv2.CAP_DSHOW),
    cv2.VideoCapture(1, cv2.CAP_DSHOW),
    cv2.VideoCapture(2, cv2.CAP_DSHOW),
    # cv2.VideoCapture(3, cv2.CAP_DSHOW),
]


while True:  # while true, read the camera
    frames = []
    for cap in captures:
        ret, frame = cap.read()
        frames.append((frame if ret else None))

    for i, frame in enumerate(frames):
        if frame is not None:  # None if not captured
            cv2.imshow(f"cam{i}", frame)

    # to break the loop and terminate the program
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

for cap in captures:
    cap.release()