#credit to ChatGPT
import cv2
import time
from PIL import Image
import numpy as np

if __name__ == '__main__':
    # Load the OD/bounding boxmodel
    model_pb = "frozen_inference_graph.pb"
    model_pbtxt = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    net = cv2.dnn_DetectionModel(model_pb, model_pbtxt)

    #google what these mean later
    net.setInputSize(320, 320)
    net.setInputScale(1.0/127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    # Define the classes of objects that the model can detect
    class_labels = []
    with open('coco.names','r') as f:
        for line in f.readlines():
            class_labels.append(line.replace('\n',''))

    # Start capturing video from the default camera
    cap = cv2.VideoCapture(0)

    # Loop over frames from the video stream
    while True:

        # Read a frame from the video stream
        ret, frame = cap.read()

         # Detect objects in the input frame
        classes, scores, boxes = net.detect(frame, confThreshold=0.5, nmsThreshold=0.4)

        # Loop over the detected objects
        for class_id, confidence, box in zip(classes, scores, boxes):
            # Draw the bounding box around the detected object
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), thickness=2)

            print("\nDEBUG: frame data")
            print(class_id)
            print(confidence)
            print(box)
            print(f"Width: {abs(box[2] - box[0])} \nHeight: {abs(box[3] - box[1])}")
            time.sleep(1)

            ## Write the class name and confidence score on the bounding box
            label = f"{class_labels[class_id-1]}: {confidence:.2f}"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), thickness=2)

            # Crop and resize the first object with class_id == 1
            if class_id == 1:
                # Crop the object from the frame
                object_image = frame[y:y+h, x:x+w]

                # Resize the object image to 64x64
                object_image = Image.fromarray(object_image).resize((64, 64))

                print(type(object_image))
                print(type(np.array(object_image)))
                # Display the resized object image
                #object_image.show()

                # Uncomment the following line to save the resized object image to disk
                # object_image.save("object.jpg")

                # Break out of the loop to only process the first object with class_id == 1
                break

        # Show the frame with detected objects
        cv2.imshow("Object Detection", frame)
        cv2.imshow("Edited",np.array(object_image))

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
