##
## Load and start an application as a standalone process

import sys
import os

import simplejson
from rctk.toolkit import Toolkit
from rctk.util import un_unicode

class ProcessWrapper(object):
    def __init__(self, klass, stdin, stdout):
        self.stdin = stdin
        if (self.stdin == sys.stdin):
            sys.stdin = open("/dev/null", "r")
        self.stdout = stdout
        if (self.stdout == sys.stdout):
            sys.stdout = open("/dev/null", "w")
        self.tk = Toolkit(klass())
        self.tk.startupdir = os.getcwd()

    def run(self):
        while True:
            # import rpdb2; rpdb2.start_embedded_debugger("foo")
            size = int(self.stdin.readline().strip())
            message = self.stdin.read(size)
            type, rest = message.split(" ", 1)
            if type == "SERVE":
                type, data = self.tk.serve(rest)
                result = {'type':type, 'data':data}
            elif type == "HANDLE":
                print rest
                method, args_str = rest.split(" ", 1)
                ## make sure we're not passing unicode keys as keyword
                ## arguments
                args = un_unicode(simplejson.loads(args_str))
                result = self.tk.handle(method, **args)
            else:
                ## wtf?
                pass

            message = simplejson.dumps(result)
            self.stdout.write("%d\n%s" % (len(message), message))
            self.stdout.flush()

def main():
    # preserve original sys.stdin/sys.stdout and redirect them to something safe.
    stdin = sys.stdin
    sys.stdin = open("/dev/null", "r")
    stdout = sys.stdout
    sys.stdout = sys.stderr = open("/tmp/out.txt", "w")
    
    appid = sys.argv[1]
    m, k = appid.rsplit('.', 1)
    mod = __import__(m, fromlist=[k])
    klass = getattr(mod, k)

    ProcessWrapper(klass, stdin, stdout).run()

if __name__ == '__main__':
    main()

