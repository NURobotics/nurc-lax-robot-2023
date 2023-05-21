'''
Prompt: I have a Javascript file that is using Websockets to establish a connection over which a server can transmit messages to a client (I will paste it below my problem description). I am trying to make a Python script that periodically generates a random image, then sends it to the client, using the Tornado library. Can you show me how to make a Python script that randomly generates and sends images at 1 frame per second?

Response: To accomplish your goal of sending a random image to the client at a rate of 1 frame per second, you can use the Tornado library in Python to create a WebSocket server and handle the periodic generation and sending of the image. Here's an example Python script that achieves this:
'''


#NOTE: to let Tornado know where the Javascript file is, need to use the file
#structure listed here: https://stackoverflow.com/questions/62286276/tornado-project-structure-js-files-not-being-found


import tornado
from tornado.web import RequestHandler, Application
from tornado.websocket import WebSocketHandler
from tornado.ioloop import PeriodicCallback, IOLoop

import random
import base64
import time
from PIL import Image
import os
from io import BytesIO

address = 81

# Generate a random image as a base64-encoded string
def generate_image():
    # Replace this with your own image generation code
    # Here, we're generating a random image using Pillow (PIL)
    img = Image.new('RGB', (100, 100), color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

# WebSocket handler
class MyWebSocketHandler(WebSocketHandler):
    def open(self):
        print("WebSocket opened")

        # Start a periodic callback to send an image every second
        self.callback = PeriodicCallback(self.send_image, 1000)
        self.callback.start()

    def send_image(self):
        image_data = generate_image()
        #print("Executing periodic function")
        self.write_message(image_data)
        #self.write_message("test")

    def on_message(self, message):

        #decode the message, if needed

        #interpret the different commands that the website can send
        if msg == 'emergency_stop':
            pass
        elif msg == 'home':
            pass
        elif msg == 'turn_on':
            pass

    def on_close(self):
        print("WebSocket closed")
        self.callback.stop()

# Web server handler
class MainHandler(RequestHandler):
    def get(self):
        #self.render("index.html")
        self.render("tornado_env_site.html")

# Create the application with WebSocket and Web handlers

# Start the server
if __name__ == "__main__":

    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "staticpath_folder"),        
    }
    #need to do this static url stuff for style sheets too

    #app = Application([(r"/", MainHandler), (r"/ws", MyWebSocketHandler)],settings = settings)
    app = Application([(r"/", MainHandler), (r"/ws", MyWebSocketHandler)],**settings)

    #app = tornado.web.Application(settings=settings, **kwargs)
    app.listen(address)

    print(f"Server started on http://localhost:{address}")
    IOLoop.current().start()
