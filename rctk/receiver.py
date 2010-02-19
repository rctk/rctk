import uuid
import web
import time

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

class Session(object):
    def __init__(self, tk):
        self.last_access = time.time()
        self.tk = tk

    def GET(self, data):
        self.last_access = time.time()
        return self.tk.GET(data)

    def POST(self, data):
        self.last_access = time.time()
        return self.tk.POST(data)

    def expired(self):
        return time.time() - self.last_access > (24*3600)
        
class Receiver(object):
    """ the receiver is the serverside of the RC protocol """
    def __init__(self, app, *args, **kw):
        self.sessions = {}
        self.app = app
        self.args = args
        self.kw = kw

    def cleanup_expired(self):
        expired = []
        for hash, value in self.sessions.iteritems():
            if value.expired():
                expired.append(hash)
        for hash in expired:
            print "Cleanup", hash
            del self.sessions[hash]

    def GET(self, data):
        data = data.strip()
        if data == "":
            sessionid = uuid.uuid1().hex
            tk = WebPyTK(self.app(*self.args, **self.kw))
            self.sessions[sessionid] = Session(tk)
            web.seeother('/' + sessionid + '/')
            return

        sessionid, rest = data.split('/', 1)
        session = self.sessions.get(sessionid)
        if session is None:
            web.seeother('/')
            return

        res = session.GET(rest)
        self.cleanup_expired()
        return res

    def POST(self, data):
        data = data.strip()

        sessionid, rest = data.split('/', 1)
        session = self.sessions.get(sessionid)
        if session is None:
            web.seeother('/')
            return
        res = session.POST(rest)
        self.cleanup_expired()
        return res

def app(a, *args, **kw):
    import os

    ## required for local static to work
    os.chdir(os.path.dirname(__file__))
    stateful = StatefulApp(Receiver(a, *args, **kw))
    return web.application(('/(.*)', 'receiver'), {'receiver':stateful}, autoreload=True)

def serve(a, *args, **kw):
    app(a, *args, **kw).run()

