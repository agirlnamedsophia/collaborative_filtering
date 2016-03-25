import tornado.ioloop
import tornado.web
import optparse

import redis


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello tornado!")


class CFError(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super(Exception, self).__init__(message)


class EventHandler(tornado.web.RequestHandler):
    """
        POST the required parameters
        * `actor`: id of the actor interacting
        * `entity`: id of the entity receiving
    """
    def post(self, actor, entity):
        try:
            client.set('event', actor, entity)
            self.write('success')
        except CFError as e:
            self.set_status(e.code)
            self.write(e.message)
            self.finish()


class EventMetricsHandler(tornado.web.RequestHandler):
    """ This will GET processed data metrics for events
    stored in the DB, found by event_id.
    """
    def get(self, event):
        try:
            entity = client.get(event)
            self.write('success')
        except CFError as e:
            self.set_status(e.code)
            self.write(e.message)
            self.finish()


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/event/(?P<actor>[^\/]+)/?(?P<entity>[^\/]+)?/", EventHandler),
        (r"/event_metrics/([^\/]+)", EventMetricsHandler)
    ])

if __name__ == '__main__':
    client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

    parser = optparse.OptionParser()
    parser.add_option('--port')

    options, _ = parser.parse_args()

    app = make_app()
    app.listen(int(options.port))
    tornado.ioloop.IOLoop.current().start()
