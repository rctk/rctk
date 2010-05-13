import os
import uuid
import web
import time

import simplejson

from toolkit import Toolkit

class Session(object):
    """
        Different requests from different browsers result in
        different sessions. Sessions can time out 
    """
    def __init__(self, tk):
        self.last_access = time.time()
        self.tk = tk

    def handle(self, method, **arguments):
        """ handle means handling tasks. the result is always json """
        self.last_access = time.time()
        return self.tk.handle(method, **arguments)

    def serve(self, name):
        """ serve means serving (static) content. Resources or html """
        type, data = self.tk.serve(name)
        web.header("content-type", type)
        return data

        # return open(os.path.join(os.path.dirname(__file__), "main.html"), "r").read()            

    def expired(self):
        return time.time() - self.last_access > (24*3600)
        
class WebPyDispatcher(object):
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
            del self.sessions[hash]

    def GET(self, data):
        data = data.strip()
        if data == "":
            sessionid = uuid.uuid1().hex
            tk = Toolkit(self.app(*self.args, **self.kw))
            self.sessions[sessionid] = Session(tk)
            web.seeother('/' + sessionid + '/')
            return

        sessionid, rest = data.split('/', 1)
        session = self.sessions.get(sessionid)
        if session is None:
            web.seeother('/')
            return

        res = session.serve(rest)
        self.cleanup_expired()
        return res


    def POST(self, data):
        data = data.strip()

        sessionid, rest = data.split('/', 1)
        session = self.sessions.get(sessionid)
        if session is None:
            web.seeother('/')
            return

        web.header("content-type", "application/json")
        method = rest.strip()
        arguments = web.input()

        self.cleanup_expired()
        result = session.handle(method, **arguments)
        return simplejson.dumps(result)

    def __call__(self):
        """
            web.py creates new instances of the class on each 
            request. We don't want that, so in stead we pretend
            to create a new instance, but actually just
            return self
        """
        return self

def app(a, *args, **kw):

    ## required for local static to work
    os.chdir(os.path.dirname(__file__))
    stateful = WebPyDispatcher(a, *args, **kw)
    return web.application(('/(.*)', 'receiver'), {'receiver':stateful}, autoreload=True)

def serve(a, *args, **kw):
    ## This is a bit of a hack for the VCR app, to be able to do some
    ## pre-run initialization
    cwd = os.getcwd()
    _a = app(a, *args, **kw)
    if hasattr(a, 'before_run_hook') and callable(a.before_run_hook):
        a.before_run_hook(_a, cwd)
    _a.run()

