import os
import signal
import time
import simplejson
import subprocess

from rctk.toolkit import factory, State, globalstate
from rctk.util import resolveclass
from rctk.app import check_classid
from rctk.frontend import Loader

import uuid
import sys, cgitb


class Manager(object):
    """ session manager """
    DEFAULT_FRONTEND = "rctk.jquery.frontend.JQueryFrontend"

    def __init__(self, sessionclass, classid, frontendclass=None, startupdir="", 
                 debug=False, *args, **kw):
        self.sessionclass = sessionclass
        self.classid = classid
        self.frontendclass = Loader.load(frontendclass or self.DEFAULT_FRONTEND)
        self.startupdir = startupdir
        self.debug = debug
        self.args = args
        self.kw = kw

        ##
        ## import the application class. This will allow the application
        ## to register all its non-dynamic resources
        self.appclass = resolveclass(classid)
        app_frontend = getattr(self.appclass, 'frontend', None)
        if app_frontend:
            self.frontendclass = app_frontend

        self.sessions = {}

        check_classid(self.classid)

    def index_html(self):
        return self.frontendclass.index_html()

    def serve_resource(self, path):
        return self.frontendclass.serve_resource(path)

    def serve_static(self, path):
        return self.frontendclass.serve(path)

    def workingdir(self):
        return self.frontendclass.workingdir()

    def cleanup_expired(self):
        expired = []
        for hash, value in self.sessions.iteritems():
            if value.expired():
                expired.append(hash)
        for hash in expired:
            self.sessions[hash].cleanup()
            del self.sessions[hash]

    def create(self):
        """ create a new session """
        sessionid = uuid.uuid1().hex

        self.sessions[sessionid] = self.sessionclass(self.classid, 
                                    debug=self.debug,
                                    args=self.args, 
                                    kw=self.kw, 
                                    startupdir=self.startupdir)

        return sessionid

    def get(self, id):
        """ find a session """
        return self.sessions.get(id)

class Session(object):
    """
        Different requests from different browsers result in
        different sessions. Sessions can time out 
    """
    def __init__(self, classid, debug, args, kw, startupdir):
        self.last_access = time.time()
        self.state = State()
        self.set_global_state()
        self.classid = classid
        self.debug = debug
        self.appclass = resolveclass(classid)

        self.app = self.appclass(*args, **kw)
        self.tk = factory(self.app, debug=debug)

        self.tk.startupdir = startupdir # ??
        self.crashed = False

    def set_global_state(self):
        """ make sure the global state is initialized """
        globalstate.setState(self.state)

    def handle(self, method, **arguments):
        """ handle means handling tasks. the result is always json """
        self.set_global_state()
        self.last_access = time.time()
        try:
            return self.tk.handle(method, **arguments)
        except Exception, e:
            self.crashed = True
            self.traceback = cgitb.html(sys.exc_info())
            if self.debug:
                print "A session crashed. Since you're running in debug mode, here's a traceback!"
                print
                print cgitb.text(sys.exc_info())
        return None

    def expired(self):
        return self.crashed or (time.time() - self.last_access > (24*3600))
        
    def cleanup(self):
        pass

    def serve(self, name):
        return self.tk.serve(name)

import threading

class SpawnedSession(object):
    """
        Spawn an rctk app in a separate process and proxy between the process
        and the gateway.
        This implementation still needs:
        - passing of args and startupdir (not sure if we need the latter)
        - processmanagement. Handle dead/killed childprocesses
        - cleanup. i.e. session timeout

        The communication with the spawned process is not thread safe,
        so we need to make sure only one message is sent to it at a time,
        hence the locking around write/reads to it. The lock is session-level
        so it should not block other threads/sessions
    """
    def __init__(self, classid, debug, args, kw, startupdir):
        self.last_access = time.time()
        ## provide state for completeness sake, but it won't be accessible
        ## in the spawned application, which will create its own state
        self.state = State()
        ## no need to make it available during the current execution

        ## startupdir and args currently not supported. 
        self.classid = classid
        self.debug = debug
        server = os.path.join(startupdir, "bin", "serve_process")
        if self.debug:
            cmd = [server, "--startupdir=" + startupdir, "--debug", classid]
        else:
            cmd = [server, "--startupdir=" + startupdir, classid]

        self.proc = subprocess.Popen(cmd,
                      stdin=subprocess.PIPE, 
                      stdout=subprocess.PIPE,
                      cwd=startupdir)
        self.lock = threading.Lock()
        self.crashed = False

    def handle(self, method, **arguments):
        """ handle means handling tasks. the result is always json """
        self.last_access = time.time()
        message = "HANDLE %s %s\n" % (method, simplejson.dumps(arguments))

        ## empty messages mean child closed connection (iow, dead)
        self.lock.acquire()
        try:
            self.proc.stdin.write("%d\n%s" % (len(message), message))
            self.proc.stdin.flush()
            size = int(self.proc.stdout.readline().strip())
            message = self.proc.stdout.read(size)
            self.lock.release()
        except IOError, e:
            self.crashed = True
            self.traceback = "The process died unexpectedly (%s)" % e
            self.lock.release()
            return None

        if message == '': ## also an error
            self.crashed = True
            self.traceback = "The process died unexpectedly (empty message)"
            return None

        if message.startswith("ERROR "):
            self.crashed = True
            error = simplejson.loads(message[6:])
            self.traceback = error['html']
            if self.debug:
                ### XXX use appropriate logging
                print "A spawned process crashed. Since you're running in debug mode, here's a traceback!"
                print
                print error['text']
                
            return None

        return simplejson.loads(message)


    def serve(self, name):
        """ serve means serving (static) content. Resources or html """
        message = "SERVE " + name 

        ## empty messages mean child closed connection (iow, dead)
        self.lock.acquire()
        try:
            self.proc.stdin.write("%d\n%s" % (len(message), message))
            self.proc.stdin.flush()

            ## Handle broken pipes in general, and specific errors (404) 
            ## from the process in general
            size = int(self.proc.stdout.readline().strip())
            message = self.proc.stdout.read(size)
            self.lock.release()
        except IOError, e:
            self.crashed = True
            self.traceback = "The process died unexpectedly (%s)" % e
            self.lock.release()
            return None

        if message.startswith("ERROR "):
            self.crashed = True
            error = simplejson.loads(message[6:])
            self.traceback = error['html']
            if self.debug:
                ### XXX use appropriate logging
                print "A spawned process crashed. Since you're running in debug mode, here's a traceback!"
                print
                print error['text']
                
            return None

        res = simplejson.loads(message)

        if res == {}:
            return None

        type = res['type']
        data = res['data'].decode('base64')
        return type, data

    def expired(self):
        return self.crashed or (time.time() - self.last_access > (24*3600))

    def cleanup(self):
        """ kill process, close proc stuff, etc """
        ## self.proc.terminate() is nicer, but >2.6 only 
        self.proc.stdin.close()
        self.proc.stdout.close()
        # self.proc.stderr.close()
        os.kill(self.proc.pid, signal.SIGKILL)
