import os
import uuid
import web

import simplejson

from rctk.sessions import Session, SpawnedSession
    
class WebPyGateway(object):
    """ the receiver is the serverside of the RC protocol """
    def __init__(self, classid, startupdir, sessionclass, *args, **kw):
        self.sessions = {}
        self.classid = classid
        self.args = args
        self.kw = kw
        self.startupdir = startupdir
        self.sessionclass = sessionclass

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

            self.sessions[sessionid] = self.sessionclass(self.classid, 
                                          self.args, self.kw, self.startupdir)
            web.seeother('/' + sessionid + '/')
            return

        sessionid, rest = data.split('/', 1)
        session = self.sessions.get(sessionid)
        if session is None:
            web.seeother('/')
            return

        type, data = session.serve(rest)
        web.header("content-type", type)
        self.cleanup_expired()
        return data


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

default_session = Session

def app(classid, *args, **kw):
    ## required for local static to work, keep startupdir for later use
    cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    stateful = WebPyGateway(classid, cwd, default_session, *args, **kw)
    return web.application(('/(.*)', 'receiver'), {'receiver':stateful}, autoreload=True)

def serve(classid, *args, **kw):
    app(classid, *args, **kw).run()

