import asyncio
import tornado

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

async def main():
    app = make_app()
    app.listen(8888) #type localhost:8888 into browser to see app
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())