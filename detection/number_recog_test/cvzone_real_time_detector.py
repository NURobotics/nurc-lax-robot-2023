import cv2
import numpy as np
import requests #for IP webcam
import imutils
import time

#for resizing/rescaling image; less resolution -> faster img processing
from skimage.transform import rescale, resize, downscale_local_mean

#some of the IP addresses of my phone cameras at diff places
#ipv4_url = 'http://10.0.0.164:8080/shot.jpg' #sherman apt
#ipv4_url = 'http://10.105.76.135:8080/shot.jpg' #northwestern
ipv4_url = None

#create a new class for object detector: makes member
#data and functions
class ObjectDetector:

    def __init__(self, thres_input, nms_input):
        self.thres = thres_input #0.45
        self.nms_threshold = nms_input #0.5
        #weights of mobilenet_ssd model. opencv provides us with a 
        #function that processes the weights and model by itself
        self.config_path = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        self.weights_path = 'frozen_inference_graph.pb'

    def config_video(self):
        '''sets up video self.captures for object detection
        grab an image, define parameters on the size and brightness of 
        the image. also sets default parameters for the net; required 
        to run. if you design your own model, that's when you need 
        to dork with the dnn values

        "coco" gives the class names. better to import them all from a
        file than write all 90 class names individually
        '''

        self.cap = cv2.VideoCapture(0)
        #self.cap2 = cv2.VideoCapture(2)

        #size
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        #brightness
        self.cap.set(10,150)
        
        #import the text of the class_names file and remove newline chars
        class_names = []
        class_file = 'coco.names'
        
        f = open(class_file)
        txt = f.read()
        f.close()

        txt_modified = txt.rstrip('\n')
        self.class_names = txt_modified.split('\n')

        #parameters for dnn
        self.net = cv2.dnn_DetectionModel(self.weights_path, self.config_path)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

    def gather_camdata(self, ip_url = None):
        '''get data from either laptop webcams or from phone camera
        gather data from both cameras

        if user gives an IP address, use phone cam as primary cam. else,
        use laptop webcam as primary cam
        '''

        if ip_url:

            #handle the various errors that can happen when you try
            #to get phone input: ConnectionError, InvalidURL, and more
            img_response = requests.get(ip_url)

            img_array = np.array(bytearray(img_response.content), dtype = np.uint8)

            #decode, resize and show the image data
            image = cv2.imdecode(img_array, -1)

            #testing out resizing of the image to reduce image filedata; optimize for speed
            scale_percent = 20 #best performance with an acceptable resolution
            width = int(image.shape[1] * scale_percent/100)
            height = int(image.shape[0] * scale_percent/100)
            dim = (width, height)

            image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

            image = imutils.resize(image, width=1000, height=1800)

        else:
            _, image = self.cap.read()

        #second capture, from webcam #2. may or not be active; handled later
        #_, image2 = self.cap2.read()
  

        #return image, image2
        return image, None

    def classify_objects(self, image):
        '''carry out detection and classification of objects

        first, feed our image into the neural net as testing data.
        attempt to detect objects with a certain confidence threshold above
        which we're sure there's an object

        also carries out non-maximum suppression (NMS): if two boxes describe
        the same object, remove all but the label with the max confidence 
        level. works by scanning the bounding boxes and indices of the results,
        and giving suggestions for what to keep

        Returns: image, markers_list
        '''
        try:
            classIds, confs, bboxes = self.net.detect(image, confThreshold=self.thres)
        except cv2.error:
            raise Exception("cv2 error: Cam1 may not be connected")
        #convert an array of arrays to a list of arrays
        bboxes = list(bboxes)

        #remake into a list and remove outer brackets
        confs = list(np.array(confs).reshape(1,-1)[0])
        confs = list(map(float, confs))
    
        #non-max suppression
        indices = cv2.dnn.NMSBoxes(bboxes, confs, self.thres,  nms_threshold = self.nms_threshold)

        markers_list = []
        for i in indices:

            #loop through indices, and find the bounding boxes and 
            #classifications that correspond to them
            #print(f"I: {i}")
            try:
                i = i[0]
            except:
                pass
            box = bboxes[i]
            x, y, w, h = box
            confidence = confs[i]
        
            center_coords = [((x + w)/2),((y + h)/2)]

            text_coords = (x + 10, y + 30)
            conf_coords = (x + w - 70, y + 50)

            #this extracts a certain class ID from the list of class id's,
            #then subtracts 1 because it uses indexing from 0
            classification = self.class_names[classIds[i][0]-1]
            conf_string = str(round(confidence*100, 2))

            #if(classification == "bird" or classification == "cat"):
            if(classification == "CORNER"):
                markers_list.append(center_coords)

            cv2.rectangle(image, (x,y), (x+w, y+h), color=(0,255,0), thickness=2)
            cv2.putText(image,classification, text_coords, 
                           cv2.FONT_HERSHEY_PLAIN, 1.5, (0,255,0), 2)
            #cv.putText(image,conf_string, conf_coords, 
            #               cv2.FONT_HERSHEY_PLAIN, 1.5, (0,255,0), 2)
       
        #print("\nMarkers:")
        #print(markers_list)

        #return an edited version of original image, markers list, and indices of 
        #objects detected; classIds and indices
        return image, markers_list, classIds, indices, bboxes

    def find_markers(self, markers_list):
        '''find locations of our 4 fiducial markers. check to see which ones
        are in each of the 4 quadrants of our image and define those as the 
        4 corners of our grid
        '''

        top_left = []
        top_right = []
        bottom_left = []
        bottom_right = []

        #640 by 480 are the approx. dims of our camera width
        center_x = 160 #should be 320 and 240, not sure why it isn't
        center_y = 120

        for marker in markers_list:
            if(marker[0] < center_x and marker[1] < center_y):
                top_left = marker
            elif(marker[0] > center_x and marker[1] < center_y):
                top_right = marker
            elif(marker[0] < center_x and marker[1] > center_y):
                bottom_left = marker
            elif(marker[0] > center_x and marker[1] > center_y):
                bottom_right = marker

        #this code will only work if the top left + right markers are in the frame
        #print("\nTop Left and Right:")
        #print(top_left)
        #print(top_right)

        #return the four marker locations
        return top_left, top_right, bottom_left, bottom_right

    def select_object(self, classIds, indices, bboxes, obj):
        '''Takes in a string classifier of an object, then iterates through
        the list of detected objects to find a match. Returns the coords
        of the object within the picture.
        '''

        #loop through indices, and find the bounding boxes and 
        #classifications that correspond to them
        object_coords = []
        for i in indices:
            i = i[0]

            #this extracts a certain class ID from the list of class id's,
            #then subtracts 1 because it uses indexing from 0
            classification = self.class_names[classIds[i][0]-1]
            try:
                if classification.lower() == obj.lower():
                    
                    box = bboxes[i]
                    x, y, w, h = box   
                    object_coords = [((x + w)/2),((y + h)/2)]
                    break

            except NameError:
                #print("Name error: object not defined")
                pass

        #return the coordinates of the object within the image. feed
        #this to locate_object to turn these into real-world coords
        return object_coords

    def locate_object(self, top_left, top_right, object_coords):
        '''find distance of objects from reference markers
        multiply the distance by the conversion factor, pixels to inches
        this is where location data can be sent to the arduino as well

        Returns: "coords" as a list
        '''
        coords = []

        try:
            L_x = 20.5
            x_squared_ref = (float(top_right[0]) - float(top_left[0]))**2
            y_squared_ref = (float(top_right[1]) - float(top_left[1]))**2
            conversion = L_x/(x_squared_ref + y_squared_ref)**0.5 
 
        except IndexError:
            #print("Index error: conversion
            pass

        try:
            x_dist = float(object_coords[0]) - float(top_left[0]) 
            y_dist = float(object_coords[1]) - float(top_left[1])
       
            #approximations of distance are a little off. for now, 
            # a temporary fix is given
            x_adjust = 0.95
            x_dist *= (conversion * x_adjust)
            y_dist *= conversion

            #self.coords = "(" + str(x_dist) + ", " + str(y_dist)  + ")"
            coords = [round(x_dist,2), round(y_dist,2)]

            #print("x distance: ",x_dist)
            #print("y distance: ",y_dist)
            #print("coords: ", self.coords)
            #value = self.write_read()
            #print(value) # printing the value returned

        except NameError:
            #print("Name error: conversion wasn't properly calculated")
            pass

        except IndexError:
            #print("Index error: calculating dist of object")
            pass

        finally:
            return coords


    def display(self, image, image2):
        '''display images to screen.
        camera 2 may not always be connected; error is handled here
        '''

        cv2.imshow("Camera 1", image)
        try:
            cv2.imshow("Camera 2", image2)
        except cv2.error:
            #print("CV error: data not read from camera 2")
            pass

#make a main function so that we can determine whether or not to run the code
#in this file. especially useful for the streamlit app, which imports
#the object detector class but doesn't run the exact same code

if __name__ == '__main__':

    od = ObjectDetector(0.45, 0.5)
    od.config_video()
    
    #obj = input("Enter an object: ")

    #collect data infinitely
    while True:

        img, img2 = od.gather_camdata(ipv4_url)
        #img, _ = od.gather_camdata(ipv4_url)


        #od.gather_camdata()
        img, markers_list, classIds, indices, bboxes = od.classify_objects(img)
        #img2, markers2, classIds2, indices2, bboxes2 = od.classify_objects(img2)

        #return the coords of all 4 corner markers. this is the code 
        #for object detection on our table grid
        tl, tr, bl, br = od.find_markers(markers_list)
        object = od.select_object(classIds, indices, bboxes, "apple")
        od.locate_object(tl, tr, object)

        #od.display(img, img2)
        od.display(img)

        cv2.waitKey(1)



