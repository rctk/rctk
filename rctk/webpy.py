import os
import web

import simplejson

from rctk.sessions import Manager, Session, SpawnedSession

class WebPyGateway(object):
    """ A gateway mediates between user/browser and RCTK application.
        This gateway is built on the web.py application server """
    def __init__(self, manager, use_cookies=False):
        self.manager = manager
        self.use_cookies = use_cookies

    def GET(self, data):
        data = data.strip()
        rest = ''
        session = None
        
        if data:
            if self.use_cookies:
                session = self.get_session_from_cookie()
                rest = data
            elif '/' in data:
                sessionid, rest = data.split('/', 1)		
                session = self.manager.get(sessionid)
        
        if session is None:
            sessionid = self.manager.create()
            session = self.manager.get(sessionid)
            if self.use_cookies:
                web.setcookie('rctk-sid', sessionid)
                if data:
                    web.seeother('/')
            else:
                web.seeother('/' + sessionid + '/')		
                return		
        
        resource = session.serve(rest)
        if resource is None:
            raise web.notfound()

        type, result = resource
        web.header("content-type", type)
        self.manager.cleanup_expired()
        return result
    
    def POST(self, data):
        data = data.strip()
        session = None
        
        if self.use_cookies:
            session = self.get_session_from_cookie()
            rest = data
        else:
            sessionid, rest = data.split('/', 1)		
            session = self.manager.get(sessionid)
        
        if session is None:
            web.seeother('/')
            return

        if session.crashed:
            self.manager.cleanup_expired()
            return

        web.header("content-type", "application/json")
        method = rest.strip()
        arguments = web.input()

        self.manager.cleanup_expired()
        
        result = session.handle(method, **arguments)
        if result is None:
            return simplejson.dumps([{'crash':True, 'application':session.classid, 'traceback':session.traceback}])

        return simplejson.dumps(result)

    def get_session_from_cookie(self):
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

def app(manager, use_cookies=False):
    ## required for local static to work
    os.chdir(os.path.dirname(__file__))
    gw = WebPyGateway(manager, use_cookies=use_cookies)
    return web.application(('/(.*)', 'gateway'), {'gateway':gw}, autoreload=True)

def serve(manager=Manager,  use_cookies=False):
    """ create the (webpy) app and run it """
    app(manager, use_cookies=use_cookies).run()

