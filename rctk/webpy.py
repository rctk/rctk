import os
import web

import simplejson

from rctk.sessions import Manager, Session, SpawnedSession

class WebPyGateway(object):
    """ A gateway mediates between user/browser and RCTK application.
        This gateway is built on the web.py application server """
    def __init__(self, manager):
        self.manager = manager

    def GET(self, data):
        data = data.strip()
        if data == "":
            sessionid = self.manager.create()
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

def app(manager):
    ## required for local static to work
    os.chdir(os.path.dirname(__file__))
    gw = WebPyGateway(manager)
    return web.application(('/(.*)', 'gateway'), {'gateway':gw}, autoreload=True)

def serve(manager=Manager):
    """ create the (webpy) app and run it """
    app(manager).run()

