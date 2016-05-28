import tornado.web

class UserHandler(tornado.web.RequestHandler):
    def get(self):
        print(self.request.arguments)
        self.write("Hello, world")

    def post(self):
        name = self.get_argument("name")
        print(name)
        self.write("Hello, " + name)
