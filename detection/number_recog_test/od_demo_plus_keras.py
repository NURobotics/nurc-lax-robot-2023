#credit to ChatGPT
import cv2
import time
from PIL import Image
import numpy as np

import os
import time
import random
import cv2 as cv
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.utils import class_weight

def extract_player_jersey(img, display=False):
    '''
    Get the helmet boxes for a frame and apply the model.
    If a player is predicted twice, keeps the prediction
    with the highest confidence score.
    
    NURC Lacrosse notes
    Code has been changed slightly from the NFL dataset sample code - removes
    the "find_team" aspect of the search, among some other NFL-specific tasks

    Changed what gets passed in as an argument, and removed the "iterating through
    bboxes" functionality


    '''
   
    #box_centre = int(box[0]+round((box[2]-box[0])/2))
    #jersey_box = img[box[3]-24:box[3]+40,box_centre-32:box_centre+32,:]

    #this assumes going in that img is a 64 x 64 x 3 image in numpy array form
    jersey_box = img
        
    #seems each input image has to be 64x64 for the script to work.  can try to resize
    #the image to get it to fit that case
    if jersey_box.shape!=(64,64,3):
        raise Exception("Image dimensions should be 64 x 64 x 3-color.")

    #result = model.predict(np.array([np.array(jersey_box)]))
    result = model.predict(np.array([jersey_box]))
    predicted_jersey_number = np.argmax(result)
    jersey_confidence = result[0][np.argmax(result)] 

    prediction_data = {"label": predicted_jersey_number,
                            "confidence":jersey_confidence}
    if display:
        print(predicted_player_code, jersey_confidence)
        plt.imshow(jersey_box)
        plt.show()
    
    return prediction_data

if __name__ == '__main__':
    # Load the OD/bounding box model
    model_pb = "frozen_inference_graph.pb"
    model_pbtxt = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    net = cv2.dnn_DetectionModel(model_pb, model_pbtxt)

    #load the number recognition model
    from keras.models import load_model
    model = load_model('best_model.h5')

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
            #time.sleep(1)

            ## Write the class name and confidence score on the bounding box
            label = f"{class_labels[class_id-1]}: {confidence:.2f}"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), thickness=2)

            # Crop and resize the first object with class_id == 1
            if class_id == 1:
                # Crop the object from the frame
                object_image = frame[y:y+h, x:x+w]

                # Resize the object image to 64x64
                object_image = Image.fromarray(object_image).resize((64, 64))
                object_image = np.array(object_image)
                # Display the resized object image
                #object_image.show()

                # Uncomment the following line to save the resized object image to disk
                # object_image.save("object.jpg")

                # Break out of the loop to only process the first object with class_id == 1
                #break


                #feed the resized model to the Keras model and see if there's a number
                prediction_data = extract_player_jersey(object_image,  display=False)
                print(prediction_data)

        # Show the frame with detected objects
        cv2.imshow("Object Detection", frame)
        cv2.imshow("Edited",object_image)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
