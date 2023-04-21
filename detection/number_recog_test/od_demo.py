
#a streamlit version of the object detector code used with the SCARA arm. 
#goal is to create a web app version of object detector so people can try it

from cvzone_real_time_detector import ObjectDetector
from requests.exceptions import InvalidURL
import cv2
import streamlit as st
import time

#NOTE: the streamlit app must be run by command line.
#1. open up Anaconda shell
#2. activate streamlit environment: "conda activate <shell name>",
#   I called my shell streamlit_shell
#2.5 to check that streamlit is installed in your shell, open python with
##  command "py", in Python >>>import streamlit and >>>streamlit.__version__
#   to get out of python: >>>exit() 
#3. navigate to location where your streamlit script is
#4. run streamlit app: streamlit run <script name>, my script is called
#   streamlit_app.py

if __name__ == '__main__':

    #start up app
    st.title("Real-Time Object Detection")
    #st.text("Hello! Here's a brief tutorial on how to turn your phone camera\n" 
    #    + "into a smart computer vision camera.")

    webcam_choice = st.radio('Webcam choice',
                             ('My phone', 'Demo Computer'))

    #create sliders, text boxes for manipulating params and viewing data
    #the slider produces an output value we can use as a variable
    threshold_value = st.sidebar.slider('Detection Threshold', 0.01, 0.99, 0.45, 0.01)
    nms_value = st.sidebar.slider('NMS Threshold', 0.01, 0.99, 0.5, 0.01)

    corner_markers_text = st.sidebar.empty()
    top_markers_text = st.sidebar.empty()
    arm_object_text = st.sidebar.empty()
    classifications_text = st.sidebar.empty()
    coords_text = st.sidebar.empty()

    #testing this out
    #top_markers_text.text("Location of top markers: " + str([3, 66]))

    #teach the user how to set up their phone so as to be able to run the
    #object detector with their phone
    if webcam_choice == 'My phone':
        #st.text('You will need to download an app called "IP Webcam" (Android)\n'
        #        + 'or "ipCam" (Apple) onto your phone in order to run this demo.')
        #st.text("Find the option that says 'start server' and press the button.")
        #st.text("Enter the IP address of your webcam (ex. 12.345.67.890:8080):")
        ip_url = st.text_input("Enter IP address")
        ip_url = "http://" + ip_url + "/shot.jpg"

        st.text(f"Using variable ip_url = {ip_url}")

    else:
        st.text('You chose "Demo computer"')
        ip_url = None

    ##num = st.number_input("Number", step=1)
    ##st.write(f'{num} + 1 = {num+1}')

    ##name = st.text_input("Enter your name")
    ##st.write(f'Hello {name}.')

    od = ObjectDetector(threshold_value, nms_value)
    od.config_video()

    #for showing image in a Streamlit environment
    FRAME_WINDOW = st.image([])
    url_error_shown = False
    connection_error_shown = False


        #if the user has entered an ip address, only then do we continue
    #if ip_url != "http:///shot.jpg":
    ##try:
    #    od.gather_camdata(ip_url)

    #    #if no errors, just clear out the error text box
    #    connection_error_shown = False
    #    url_error_shown = False

    #except ConnectionError:
    #    if not connection_error_shown:
        #st.error("Not connected")
    #        connection_error_shown = True

    #except InvalidURL:
    #    if not url_error_shown:
    #        st.error("Waiting to connect")
    #        url_error_shown = True
 

    while True:

        img, img2 = od.gather_camdata(ip_url)

        #if we gathered data, and img is an attribute of od, proceed
        if 'img':
            img, markers_list, classIds, indices, bboxes = od.classify_objects(img)
            tl, tr, _, _ = od.find_markers(markers_list)
            obj = od.select_object(classIds, indices, bboxes, "apple")
            od.locate_object(tl, tr, obj)

            #this takes the place of the display() function
            frame_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame_img)

            #if we detected corner markers or an object, write it into text boxes
            corner_markers_text.text("Location of markers in image: \n"
                                     + str(markers_list))
            top_markers_text.text("Location of top markers: \n" 
                                    + str(tl) + '\n' + str(tr))
            #arm_object_text.text("Arm object: \n" + str(od.arm_object))
  
            #display all the classifications detected to the screen.
            #see ObjectDetector class for more detail on how this works
            classifications = [od.class_names[classIds[i][0][0]-1] 
                               for i in indices]
            classes_stylized = ''
            for x in classifications:
                classes_stylized += x + ' \n'

            classifications_text.text("Objects detected: \n" + classes_stylized)

            #if we found a distance of the object from corner markers,
            #display it to the screen
            if 'coords' in dir(od):
                pass

        #if we've gotten here, we've gathered cam data hopefully

        #nah, the error happens and then the rest of the code begins to
        #execute. that means I can't use the error as a breakpoint


        #od.gather_camdata(ip_url)
        #time.sleep(1)
        #st.text("Waiting 1 sec")

