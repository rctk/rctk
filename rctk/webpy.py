import os
import uuid
import web
import time

import simplejson

from toolkit import Toolkit

def resolveclass(classid):
    m, k = classid.rsplit(".", 1)
    mod = __import__(m, fromlist=[k])
    klass = getattr(mod, k)
    return klass

class Session(object):
    """
        Different requests from different browsers result in
        different sessions. Sessions can time out 
    """
    def __init__(self, classid, args, kw, startupdir):
        self.last_access = time.time()
        self.app = resolveclass(classid)
        self.tk = Toolkit(self.app(*args, **kw))
        self.tk.startupdir = startupdir

    def handle(self, method, **arguments):
        """ handle means handling tasks. the result is always json """
        self.last_access = time.time()
        return self.tk.handle(method, **arguments)

    def serve(self, name):
        """ serve means serving (static) content. Resources or html """
        type, data = self.tk.serve(name)
        web.header("content-type", type)
        return data

    def expired(self):
        return time.time() - self.last_access > (24*3600)
        
import subprocess

class SpawnedSession(object):
    """
        Spawn an rctk app in a separate process and proxy between the process
        and web.py.
        This implementation still needs:
        - passing of args and startupdir (not sure if we need the latter)
        - processmanagement. Handle dead/killed childprocesses
        - cleanup. i.e. session timeout
    """
    def __init__(self, classid, args, kw, startupdir):
        self.last_access = time.time()
        ## startupdir and args currently not supported. 
        server = os.path.join(startupdir, "bin", "serve_process")
        self.proc = subprocess.Popen([server, classid],
                      stdin=subprocess.PIPE, 
                      stdout=subprocess.PIPE)

    def handle(self, method, **arguments):
        """ handle means handling tasks. the result is always json """
        self.last_access = time.time()
        message = "HANDLE %s %s\n" % (method, simplejson.dumps(arguments))
        self.proc.stdin.write("%d\n%s" % (len(message), message))
        self.proc.stdin.flush()

        size = int(self.proc.stdout.readline().strip())
        message = self.proc.stdout.read(size)
        return simplejson.loads(message)


    def serve(self, name):
        """ serve means serving (static) content. Resources or html """
        message = "SERVE " + name 
        self.proc.stdin.write("%d\n%s" % (len(message), message))
        self.proc.stdin.flush()

        size = int(self.proc.stdout.readline().strip())
        message = self.proc.stdout.read(size)
        res = message
        res = simplejson.loads(res)
        type = res['type']
        data = res['data']
        web.header("content-type", type)
        return data


    def expired(self):
        return time.time() - self.last_access > (24*3600)
    
class WebPyDispatcher(object):
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

            self.sessions[sessionid] = self.sessionclass(self.classid, self.args, self.kw, self.startupdir)
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

default_session = Session

def app(classid, *args, **kw):
    ## required for local static to work, keep startupdir for later use
    cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    stateful = WebPyDispatcher(classid, cwd, default_session, *args, **kw)
    return web.application(('/(.*)', 'receiver'), {'receiver':stateful}, autoreload=True)

def serve(classid, *args, **kw):
    app(classid, *args, **kw).run()

