import os
import web

import simplejson

from rctk.sessions import Manager, Session, SpawnedSession

class WebPyGateway(object):
    """ A gateway mediates between user/browser and RCTK application.
        This gateway is built on the web.py application server """
    def __init__(self, classid, startupdir, manager, *args, **kw):
        self.classid = classid
        self.args = args
        self.kw = kw
        self.startupdir = startupdir
        self.manager = manager


    def GET(self, data):
        data = data.strip()
        if data == "":
            sessionid = self.manager.create(self.classid, self.args, self.kw, self.startupdir)
            web.seeother('/' + sessionid + '/')
            return

        sessionid, rest = data.split('/', 1)
        session = self.manager.get(sessionid)
        if session is None:
            web.seeother('/')
            return

        type, data = session.serve(rest)
        web.header("content-type", type)
        self.manager.cleanup_expired()
        return data


    def POST(self, data):
        data = data.strip()

        sessionid, rest = data.split('/', 1)
        session = self.manager.get(sessionid)
        if session is None:
            web.seeother('/')
            return

        web.header("content-type", "application/json")
        method = rest.strip()
        arguments = web.input()

        self.manager.cleanup_expired()
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

def app(classid, manager, *args, **kw):
    ## required for local static to work, keep startupdir for later use
    cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    stateful = WebPyGateway(classid, cwd, manager(default_session), *args, **kw)
    return web.application(('/(.*)', 'receiver'), {'receiver':stateful}, autoreload=True)

def serve(classid, manager=Manager, *args, **kw):
    """ create the (webpy) app and run it """
    app(classid, manager, *args, **kw).run()

