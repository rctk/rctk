import os
import web

import simplejson

from rctk.sessions import Manager

class WebPyGateway(object):
    """ A gateway mediates between user/browser and RCTK application.
        This gateway is built on the web.py application server """
    def __init__(self, manager):
        self.manager = manager

    def GET(self, data):
        """
            GET serves content that's considered static and
            cachable, not related to a specific session 
            is requested, a new session will be started
        """
        data = data.strip()
        session = None
        
        ## python-static stuff (not related to a session) will not work with
        ## spawned processes. It would mean the manager is able to handle
        ## these requests locally, without a session. This may not be the 
        ## case for dynamic resources.
        if not data: ## should be related to a session / create a session
            web.header("Content-Type", "text/html")
            return self.manager.index_html()

        if data.startswith("media"):
            ## set cachable headers?
            type, result = self.manager.serve_static(data)
            web.header("Content-Type", type)
            return result

        if data.startswith("resources/"):
            type, result = self.manager.serve_resource(data)
            web.header("Content-Type", type)
            return result

        if not data.startswith("dynamic/"):
            raise web.notfound()

        ## app instance specific dynamic data, eg images from database,
        ## music. Requires sessionid, which must be passed as an argument
        sessionid = web.input(name='sessionid')
        session = self.manager.get(sessionid)
        
        if session is None:
            raise web.notfound()
        elif session.crashed:
            self.manager.cleanup_expired()
            web.seeother('/')
            return

        web.header('rctk-sid', sessionid)
        resource = session.serve(data)
        self.manager.cleanup_expired()

        if resource is None:
            raise web.notfound()

        type, result = resource
        web.header("Content-Type", type)

        ## experimental partial content support
        ## perhaps this shouldn't be enabled by default
        # return result ## XXX partial support disabled!
        
        ## doesn't seem to work with chrome - works better without, actually.
        ## Let's disable for now.
        range = web.ctx.env.get('HTTP_RANGE')
        if range is None:
            return result

        total = len(result)
        _, r = range.split("=")
        partial_start, partial_end = r.split("-")

        start = int(partial_start)

        if not partial_end:
            end = total-1
        else:
            end = int(partial_end)

        ## ignore "small" startrequests. Not sure why this is needed.
        if end < 2000:
            end = total-1

        chunksize = (end-start)+1

        web.ctx.status = "206 Partial Content"
        web.header("Accept-Ranges", "bytes")
        web.header("Content-Length", str(chunksize))
        web.header("Content-Range", "bytes %d-%d/%d" % (start, end, total))
        web.header("Connection", "close")
        return result[start:end+1]        
    
    def POST(self, data):
        # import pdb; pdb.set_trace()
        data = data.strip()
        session = None
        
        sessionid = web.ctx.environ.get('HTTP_RCTK_SID')
        session = self.manager.get(sessionid)
        
        if session is None:
            sessionid = self.manager.create()
            session = self.manager.get(sessionid)
        elif session.crashed:
            self.manager.cleanup_expired()
            web.seeother('/')
            return

        web.header('rctk-sid', sessionid)
        web.header("Content-Type", "application/json")
        method = data.strip()
        arguments = web.input()
        
        result = session.handle(method, **arguments)

        self.manager.cleanup_expired()

        if result is None:
            return simplejson.dumps([{'crash':True, 'application':session.classid, 'traceback':session.traceback}])

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
    os.chdir(manager.workingdir())
    gw = WebPyGateway(manager)
    return web.application(('/(.*)', 'gateway'), {'gateway':gw}, autoreload=True)

def serve(manager=Manager):
    """ create the (webpy) app and run it """
    app(manager).run()

