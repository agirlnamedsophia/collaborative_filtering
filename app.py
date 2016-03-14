import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello tornado!")


class CFError(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super(Exception, self).__init__(message)


class EventHandler(tornado.web.RequestHandler):
    """ This will POST an interaction between
    the players to the database
    """
    def post(self, actor, entity):
        try:
            self.write('POST with an actor and entity')
        except CFError as e:
            self.set_status(e.code)
            self.write(e.message)
            self.finish()


class EventMetricsHandler(tornado.web.RequestHandler):
    """ This will GET processed data metrics for events
    stored in the DB, found by event_id.
    """
    def get(self, event_id):
        try:
            self.write('Here is where we fetch an event metric')
        except CFError as e:
            self.set_status(e.code)
            self.write(e.message)
            self.finish()


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/event/(?P<actor>[^\/]+)/?(?P<entity>[^\/]+)?/", EventHandler),
        (r"/event_metrics/(\d+)", EventMetricsHandler)
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
