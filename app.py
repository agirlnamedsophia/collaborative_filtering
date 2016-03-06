import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello tornado!")


class RecommendationHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('GET - Susie will like this because Jane did, too')


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/recommendation/?", RecommendationHandler)
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
