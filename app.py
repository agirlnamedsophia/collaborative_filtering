import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello tornado!")


class EventHandler(tornado.web.RequestHandler):
    """ This will POST to the database the players
    in an interaction that will then be analyzed.
    """
    def post(self, actor, entity):
        try:
            self.write('POST with an actor and entity')
        except OSError as e:
            self.respond(e.message, e.code)


class EventMetricsHandler(tornado.web.RequestHandler):
    """ This will GET processed data metrics for events
    stored in the DB, found by event_id.
    """
    def get(self, event_id):
        try:
            event = retrieve_from_db(event_id)
            self.write(event.serialize())
        except OSError as e:
            self.respond(e.message, e.code)


def respond(self, data, code=200):
    self.set_status(code)
    self.write(JSONEncoder().encode({
        "status": code,
        "data": data
    }))
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
