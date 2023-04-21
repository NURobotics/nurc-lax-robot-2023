
#a streamlit version of the object detector code used with the SCARA arm. 
#goal is to create an app interface for controlling bot

from requests.exceptions import InvalidURL
import cv2
import streamlit as st
import time

from cvzone_real_time_detector import ObjectDetector
import pyduino as pyd

#NOTE: the streamlit app must be run by command line.
#1. open up Anaconda shell
#2. activate streamlit environment: "conda activate <shell name>",
#   I called my shell streamlit_shell
#2.5 to check that streamlit is installed in your shell, open python with
##  command "py", in Python >>>import streamlit and >>>streamlit.__version__,
#   then to get out of python: >>>exit() 
#3. navigate to location where your streamlit script is
#4. run streamlit app: streamlit run <script name>, my script is called
#   streamlit_app.py for example

if __name__ == '__main__':

    #start up app
    st.title("Robotic Object Detection")
    st.text("Using an overhead camera and side cam " \
            + "to detect what's in front of the bot")
    home = st.checkbox("Homing sequence")

    #create sliders, text boxes for manipulating params and viewing data
    #the slider produces an output value we can use as a variable
    threshold_value = st.sidebar.slider('Detection Threshold', 0.01, 0.99, 0.45, 0.01)
    nms_value = st.sidebar.slider('NMS Threshold', 0.01, 0.99, 0.5, 0.01)

    corner_markers_text = st.sidebar.empty()
    top_markers_text = st.sidebar.empty()
    arm_object_text = st.sidebar.empty()
    classifications_text = st.sidebar.empty()

    #testing this out
    ip_url = None #not using the phone webcam
    #ip_url = "http://10.0.0.164:8080/shot.jpg"

    od = ObjectDetector(threshold_value, nms_value)
    od.config_video()

    #for showing image in a Streamlit environment
    url_error_shown = False
    connection_error_shown = False

    #two columns to show two images side by side
    col1, col2 = st.columns(2)
    WINDOW1 = col1.image([])
    WINDOW2 = col2.image([])

    #button to get commands sent to the robot
    run_command = st.checkbox('Run robot')

    #text to show what the arduino data will be
    cv_coords_text = st.empty()
    robot_coords_text = st.empty()
    arduino_data_txt = st.empty()

    #object selected
    obj_type = "apple"

    #sort of like a frame tracker for the amount of time 
    #we have had the "run command" button up
    n_iters = 0

    while True:

        img, img2 = od.gather_camdata(ip_url)
        #img, _ = od.gather_camdata(ip_url)


        #if we gathered data, proceed
        if 'img':

            #option to classify object in both views of the cam
            img, markers_list, classIds, indices, bboxes = od.classify_objects(img)
            #img2, _, _, _, _ = od.classify_objects(img2)

            #find corner markers; coordinates of object in diff. ref frames
            tl, tr, _, _ = od.find_markers(markers_list)
            obj_coords = od.select_object(classIds, indices, bboxes, obj_type)
            cv_coords = od.locate_object(tl, tr, obj_coords)
            robot_coords = pyd.convert_coords(cv_coords)

            #this takes the place of the display() function
            frame1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #frame2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            WINDOW1.image(frame1)
            #WINDOW2.image(frame2)
  
            #display all the classifications detected to the screen.
            #see ObjectDetector class for more detail on how this works
            classifications = [od.class_names[classIds[i][0][0]-1] 
                               for i in indices]
            classes_stylized = ''
            for x in classifications:
                classes_stylized += x + ' \n'


            #if we detected corner markers or an object, write it into text boxes
            top_markers_text.text("Location of top markers: \n" 
                                    + str(tl) + '\n' + str(tr))

            #displaying the most important data
            classifications_text.text("Objects detected (top view): \n" + classes_stylized)
            arm_object_text.text("Selected object: \n" + obj_type)
            cv_coords_text.text("Grid coords of object: \n" + str(cv_coords))
            robot_coords_text.text("Robot's coords of object: \n" + str(robot_coords))

            #if we found object coords and we press a button, send 
            #commands to the robot

            #streamlit scripts usually run from top to bottom even if 
            #widgets are pressed, so it should
            #be able to execute the button-controlled logic. after that, it'll
            #reset the script (as streamlit widgets generally cause)
            if run_command:

                #alright, so the way it works: when you press the button
                #in streamlit, the whole script restarts, and then the 
                #button is pressed permanently. could be managed by a 
                #check of if this is the first iteration or not
                #
                #I want to try using a checkbox too, so that we can turn 
                #off the button without restarting the app 
                #print("Got to this control statement")

                if not robot_coords:
                    n_iters = 0 #rset the count
                    continue

                [x,y] = robot_coords
                j1, j2, j3 = pyd.inverse_kinematics(x,y)
                arduino_text = pyd.format_commands(j1,j2,j3,0,90)

                arduino_data_txt.text("Text to send to Arduino: \n" \
                    + arduino_text)

                #send the joint angles to the arduino only once
                if n_iters == 0:
                   pyd.write_read_arduino(arduino_text)

                n_iters += 1

            elif home:
                #send data to the arduino so it causes homing 
                #function to activate
                arduino_text = "0,1,0,0,0,0,0,500,500"
                arduino_data_txt.text("Text to send to Arduino: \n" \
                        + arduino_text)

                pyd.write_read_arduino(arduino_text)

            else:
                n_iters = 0



            #    if not robot_coords:
            #        continue