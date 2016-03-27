import tornado.ioloop
import tornado.web
import optparse

import redis


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello tornado!")


class CFError(Exception):
    pass
    self.message = message
    self.code = code


class EventHandler(tornado.web.RequestHandler):
    """
        POST the required parameters
        actor (int): id of the actor interacting
        entity (int): id of the entity receiving
    """
    def post(self, actor, entity):
        try:
            client.set('event', actor, entity)
            self.write('success')
        except CFError as e:
            self.set_status(e.code)
            self.write(e.message)


class EventMetricsHandler(tornado.web.RequestHandler):
    """
        GET processed data metrics for events
        event (int): id of event
    """
    def get(self, event):
        try:
            entity = client.get(event)
            self.write('success')
        except CFError as e:
            self.set_status(e.code)
            self.write(e.message)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"^event/$", EventHandler),
        (r"^/event_metrics/([0-9]+)/$", EventMetricsHandler)
    ])

if __name__ == '__main__':
    client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

    parser = optparse.OptionParser()
    parser.add_option('--port')

    options, _ = parser.parse_args()

    app = make_app()
    app.listen(int(options.port))
    tornado.ioloop.IOLoop.current().start()
