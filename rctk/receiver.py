import uuid
import web

from toolkit import WebPyTK


class StatefulApp(object):
    """ once created it will reuse the same instance
        for each request """

    def __init__(self, app):
        self.app = app

    def GET(self, data):
        return self.app.GET(data)

    def POST(self, data):
        return self.app.POST(data)

    def __call__(self):
        return self.app

class Receiver(object):
    """ the receiver is the serverside of the RC protocol """
    def __init__(self, app, *args, **kw):
        self.sessions = {}
        self.app = app
        self.args = args
        self.kw = kw

    def GET(self, data):
        data = data.strip()
        if data == "":
            sessionid = uuid.uuid1().hex
            tk = WebPyTK(self.app(*self.args, **self.kw))
            self.sessions[sessionid] = tk
            web.seeother('/' + sessionid + '/')
            return

        sessionid, rest = data.split('/', 1)
        session = self.sessions[sessionid]
        return session.GET(rest)

    def POST(self, data):
        data = data.strip()

        sessionid, rest = data.split('/', 1)
        session = self.sessions[sessionid]
        return session.POST(rest)

def app(a, *args, **kw):
    import os

    ## required for local static to work
    os.chdir(os.path.dirname(__file__))
    stateful = StatefulApp(Receiver(a, *args, **kw))
    return web.application(('/(.*)', 'receiver'), {'receiver':stateful}, autoreload=True)

def serve(a, *args, **kw):
    app(a, *args, **kw).run()

