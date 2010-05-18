import time
import simplejson
import subprocess
from rctk.toolkit import Toolkit
from rctk.util import resolveclass

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
        return type, data

    def expired(self):
        return time.time() - self.last_access > (24*3600)
        
    def cleanup(self):
        pass

class SpawnedSession(object):
    """
        Spawn an rctk app in a separate process and proxy between the process
        and the gateway.
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
        return type, data

    def expired(self):
        return time.time() - self.last_access > (24*3600)

    def cleanup(self):
        """ kill process, close proc stuff, etc """
        pass
