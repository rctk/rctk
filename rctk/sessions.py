import os
import time
import simplejson
import subprocess
from rctk.toolkit import Toolkit, State, globalstate
from rctk.util import resolveclass

import uuid

class Manager(object):
    """ session manager """
    def __init__(self, sessionclass):
        self.sessionclass = sessionclass
        self.sessions = {}

    def cleanup_expired(self):
        expired = []
        for hash, value in self.sessions.iteritems():
            if value.expired():
                expired.append(hash)
        for hash in expired:
            self.sessions[hash].cleanup()
            del self.sessions[hash]

    def create(self, classid, args, kw, startupdir):
        """ create a new session """
        sessionid = uuid.uuid1().hex

        self.sessions[sessionid] = self.sessionclass(classid, 
                                      args, kw, startupdir)

        return sessionid

    def get(self, id):
        """ find a session """
        return self.sessions.get(id)

class Session(object):
    """
        Different requests from different browsers result in
        different sessions. Sessions can time out 
    """
    def __init__(self, classid, args, kw, startupdir):
        self.last_access = time.time()
        self.state = State()
        self.set_global_state()
        self.app = resolveclass(classid)
        self.tk = Toolkit(self.app(*args, **kw))
        self.tk.startupdir = startupdir

    def set_global_state(self):
        """ make sure the global state is initialized """
        globalstate.setState(self.state)

    def handle(self, method, **arguments):
        """ handle means handling tasks. the result is always json """
        self.set_global_state()
        self.last_access = time.time()
        return self.tk.handle(method, **arguments)

    def serve(self, name):
        """ serve means serving (static) content. Resources or html """
        self.set_global_state()
        type, data = self.tk.serve(name)
        return type, data

    def expired(self):
        return time.time() - self.last_access > (24*3600)
        
    def cleanup(self):
        pass

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
    def __init__(self, classid, args, kw, startupdir):
        self.last_access = time.time()
        ## provide state for completeness sake, but it won't be accessible
        ## in the spawned application, which will create its own state
        self.state = State()
        ## no need to make it available during the current execution

        ## startupdir and args currently not supported. 
        server = os.path.join(startupdir, "bin", "serve_process")
        self.proc = subprocess.Popen([server, classid],
                      stdin=subprocess.PIPE, 
                      stdout=subprocess.PIPE)
        self.lock = threading.Lock()

    def handle(self, method, **arguments):
        """ handle means handling tasks. the result is always json """
        self.last_access = time.time()
        message = "HANDLE %s %s\n" % (method, simplejson.dumps(arguments))

        ## empty messages mean child closed connection (iow, dead)
        self.lock.acquire()
        self.proc.stdin.write("%d\n%s" % (len(message), message))
        self.proc.stdin.flush()

        size = int(self.proc.stdout.readline().strip())
        message = self.proc.stdout.read(size)
        self.lock.release()

        return simplejson.loads(message)


    def serve(self, name):
        """ serve means serving (static) content. Resources or html """
        message = "SERVE " + name 

        ## empty messages mean child closed connection (iow, dead)
        self.lock.acquire()
        self.proc.stdin.write("%d\n%s" % (len(message), message))
        self.proc.stdin.flush()

        size = int(self.proc.stdout.readline().strip())
        message = self.proc.stdout.read(size)
        self.lock.release()

        res = simplejson.loads(message)
        type = res['type']
        data = res['data']
        return type, data

    def expired(self):
        return time.time() - self.last_access > (24*3600)

    def cleanup(self):
        """ kill process, close proc stuff, etc """
        pass
