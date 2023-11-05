import cv2
import numpy as np

def get_hsv_range(event, x, y, flags, param):
    global hsv_value
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_pixel = hsv_frame[y, x]
        lower_hsv = np.array([hsv_pixel[0] - 10 , hsv_pixel[1] - 10, hsv_pixel[2] - 10])
        upper_hsv = np.array([hsv_pixel[0] + 10, hsv_pixel[1] + 10, hsv_pixel[2] + 10])
        print("Lower HSV Range:", lower_hsv)
        print("Upper HSV Range:", upper_hsv)
        hsv_value = lower_hsv, upper_hsv

# Create a VideoCapture object to capture video from your camera
cap = cv2.VideoCapture(0)  # You may need to adjust the index (0 for the default camera)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Couldn't open the camera.")
    exit()

# Create a window to display the video stream
cv2.namedWindow('Video Stream')
cv2.setMouseCallback('Video Stream', get_hsv_range)

hsv_value = None
hsv_values = []

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Couldn't read a frame.")
        break

    # Convert the frame to the HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if hsv_value is not None:
        #TODO : Store the max and min value per loop and only check updated values with the new min and max
        # Check if there is a new hsv value
        #if hsv_value != hsv_values[-1]:
            # hsv_values.append(hsv_value)

            # Compute new lower and upper bounds just by checking based on the new hsv points
            #lower_hsv = np.array([min([lower_hsv[0],hsv_value[0][0]]),min([lower_hsv[1],hsv_value[0][1]]),min([lower_hsv[2],hsv_value[0][2]])])
            #upper_hsv = np.array

        lower_hsv, upper_hsv = hsv_value
        # lower_hsv = np.array([min(hsv[0] for hsv in hsv_values), min(hsv[1] for hsv in hsv_values), min(hsv[2] for hsv in hsv_values)])
        # upper_hsv = np.array([max(hsv[0] for hsv in hsv_values), max(hsv[1] for hsv in hsv_values), max(hsv[2] for hsv in hsv_values)])
        mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow('Selected Region', result)

    cv2.imshow('Video Stream', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close all windows
cap.release()
cv2.destroyAllWindows()
