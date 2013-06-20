#!/usr/bin/env python
import os.path
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json

# import and define tornado-y things
from tornado.options import define
define("port", default=5000, help="run on the given port", type=int)

archived_strokes = []

class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            (r"/?", MainHandler),
            (r"/api/archive_strokes/?", APIArchiveStrokesHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )

        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        google_analytics_id = os.environ['GOOGLEANALYTICSID'] if 'GOOGLEANALYTICSID' in os.environ else False

        self.render(
            "main.html",
            google_analytics_id=google_analytics_id,
            strokes=archived_strokes
        )


class APIArchiveStrokesHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument('username')
        password_hash = self.get_argument('password_hash')
        instance_name = self.get_argument('instance_name')
        buff = json.loads(self.get_argument('buff'))

        archived_strokes.append({
            'username': username,
            'password_hash': password_hash,
            'instance_name': instance_name,
            'buff': buff
        })


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
