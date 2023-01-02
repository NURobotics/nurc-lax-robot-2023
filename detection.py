# Usage

# python3 ball_detect_track.py --input videos/8Meters_Center1.avi

# import packages
import cv2
import numpy as np
import argparse
import os
import imutils
import time
import datetime
import matplotlib.pyplot as plt
from collections import OrderedDict
from centroid_tracker import CentroidTracker
import matplotlib.pyplot as plt
from visualize_tracking import visualize

# TODO: Cythonize this
def detection_and_tracking(vid_input, yolo_net, layerNames, confid, threshold, disappeared, tracking=False):
    # if no video input, use computer webcam
    if vid_input is None:
        print("Loading Webcam...")
        vs = cv2.VideoCapture(0)
        time.sleep(2.0)
    else:
        print("Loading Video...")
        vs = cv2.VideoCapture(vid_input)

    cv2.startWindowThread()
    cv2.namedWindow('tracking', cv2.WINDOW_NORMAL)

    # initializing:
    (H, W) = (None, None)  # frame dimensions
    frameCount = 0  # keep track of number of frames analyzed so far
    ct = CentroidTracker(maxDisappeared=disappeared)  # centroid tracker

    # loop over each frame in video
    while True:
        (grabbed, frame) = vs.read()

        # break if using video input and no frame left to grab
        if args["input"] is not None and frame is None:
            print("End of Video File")
            break

        # resizing frames for consistency, regardless of size of input video
        frame = imutils.resize(frame, width=1250)

        # grabbing frame dimensions
        if W is None or H is None:
            (H, W) = frame.shape[:2]

        # YOLO Detection
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        yolo_net.setInput(blob)
        layerOutputs = yolo_net.forward(layerNames)

        boxes = []
        confidences = []
        classIDs = []

        # loop over each detection
        for output in layerOutputs:
            for detection in output:
                # extract the class ID and confidence of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filtering detections to just people with confidence above minimum confidence argument
                if classID == 0 and confidence > confid:
                    # scale the bounding box coordinates back relative to the size of the image
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # calculate coordinates of top left point of box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maximum suppression algorithm and store final results in bounding box list
        nms_boxes = cv2.dnn.NMSBoxes(boxes, confidences, confid, threshold)
        boundingboxes = []
        for i in range(len(boxes)):
            if i in nms_boxes:
                boundingboxes.append(boxes[i])

        print("first: ", boundingboxes)
        # call update function in centroid tracker, draw unique ID above bounding box

        if tracking:
            objects = ct.update(frame, boundingboxes)
            # turning ordered dictionary into list of tuples
            boundingboxes = [(ID, box) for ID, box in objects.items()]
        else:
            boundingboxes = [(ID, box) for ID, box in enumerate(boundingboxes)]

        print("second: ", boundingboxes)

        w_boxes = visualize(frame, boundingboxes)
        cv2.imshow("tracking", w_boxes)

        # update frame count
        frameCount = frameCount + 1

        # press 'q' to end program before video ends
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release video capture and destroy all windows
    vs.release()
    cv2.destroyAllWindows()


# constructing argument parser and parsing arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str,
                help="path to input video")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
                help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
                help="threshold when applying non-maximum suppression")
ap.add_argument("-d", "--disappeared", type=int, default=10,
                help="number of frames that an object ID is not detected before it is de-registered")
ap.add_argument("-tr", "--tracking", type=int, default=False,
                help="number of frames between data output to text file")
args = vars(ap.parse_args())

# deriving the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join(["yolo-balls", "yolov3.weights"])
configPath = os.path.sep.join(["yolo-balls", "yolov3.cfg"])

# loading YOLO object detector
print("Loading YOLO From Disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
# calling SDD function
detection_and_tracking(args["input"], net, ln, args["confidence"], args["threshold"],
                       args["disappeared"], args["tracking"])
