import tornado
import tornado.web
import tornado.websocket
import tornado.ioloop
import base64
import io
from PIL import Image

# Create a handler for the homepage
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('/WebPages/ShotHistory.html')

# Create a handler for the websocket connection
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('WebSocket opened')

    def on_message(self, message):
        if message == 'get-png-image':
            # Generate a PNG image
            image = Image.new('RGBA', (200, 200), color='red')
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            png_data = buffer.getvalue()

            # Encode the PNG image data as base64 and send it over the websocket
            png_base64 = base64.b64encode(png_data).decode('utf-8')
            self.write_message(png_base64)

    def on_close(self):
        print('WebSocket closed')

# Create a Tornado application
app = tornado.web.Application([
    (r'/', MainHandler),
    (r'/websocket', WebSocketHandler),
], WebPage_path='WebPages')

# Start the Tornado server
if __name__ == '__main__':
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
