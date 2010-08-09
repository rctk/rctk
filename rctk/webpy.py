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
        session = self.get_active_session()
        
        if session is None:
            sessionid = self.manager.create()
            web.setcookie('rctk-sid', sessionid)
            web.seeother('/')
            return

        type, result = session.serve(data.strip())
        web.header("content-type", type)
        self.manager.cleanup_expired()
        return result
    
    def POST(self, data):
        session = self.get_active_session()

        if session is None:
            web.seeother('/')
            return

        web.header("content-type", "application/json")
        method = data.strip()
        arguments = web.input()

        self.manager.cleanup_expired()
        try:
            result = session.handle(method, **arguments)
        except:
            # TODO: something has gone wrong, find out what and handle session cleanup or recovery.
            pass
        return simplejson.dumps(result)

    def get_active_session(self):
        """ Use a cookie to find out if the client already has an active session.
            Returns the session or None if valid session is found.
        """
        sessionid = web.cookies().get('rctk-sid')
        if sessionid:
            session = self.manager.get(sessionid)
            if session is None:
                # user has a cookie, but no session present so delete the cookie
                web.setcookie('rctk-sid', sessionid, expires=-84000)
            else:
                return session
        return None    

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

