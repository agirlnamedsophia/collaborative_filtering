import tornado.ioloop
import tornado.web
import optparse

import redis

from settings import REDIS_HOST, REDIS_PORT

client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello tornado!")


class EventHandler(tornado.web.RequestHandler):
    """
        POST the required parameters
        actor (int): id of the actor interacting
        entity (int): id of the entity receiving
    """
    def post(self, actor, entity):
        r = client
        # what should the key be?
        key = 'fave:%s' % entity
        event = r.sadd(key, actor, entity)
        members = r.smembers(key)
        response = { 'id': event,
                     'members': list(members) }
        self.write(response)


class EventMetricsHandler(tornado.web.RequestHandler):
    """
        GET processed data metrics for events
        event (int): id of event
    """
    def get(self, event):
        r = client
        # what is the event here? how do we calculate values?
        metrics = r.zadd('event', 1, event)
        entity = r.zrange('event', 0, -1, withscores=True)
        response = { 'id': int(event),
                     'name': entity }
        self.write(response)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/event/(\d+)/(\d+)$", EventHandler),
        (r"/event_metrics/(\d+)$", EventMetricsHandler)
    ])

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--port')

    options, _ = parser.parse_args()

    app = make_app()
    app.listen(int(options.port))
    tornado.ioloop.IOLoop.current().start()
