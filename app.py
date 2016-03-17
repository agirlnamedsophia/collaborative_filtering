import tornado.ioloop
import tornado.web

import optparse


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello tornado!")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--port')

    options, _ = parser.parse_args()

    app = make_app()
    app.listen(int(options.port))
    tornado.ioloop.IOLoop.current().start()