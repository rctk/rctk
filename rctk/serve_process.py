##
## Load and start an application as a standalone process

import sys
import os

import simplejson
from rctk.toolkit import Toolkit

class ProcessWrapper(object):
    def __init__(self, klass):
        self.tk = Toolkit(klass())
        self.tk.startupdir = os.getcwd()
        self.stdin = sys.stdin
        self.stdout = sys.stdout

        print >> sys.stderr, "Hello world"
        sys.stdin = open("/dev/null", "r")
        sys.stdout = open("/dev/null", "w")

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
                method, args_str = rest.split(" ", 1)
                args = simplejson.loads(args_str)
                result = self.tk.handle(method, **args)
            else:
                ## wtf?
                pass

            message = simplejson.dumps(result)
            self.stdout.write("%d\n%s" % (len(message), message))
            self.stdout.flush()

def main():
    appid = sys.argv[1]
    m, k = appid.rsplit('.', 1)
    mod = __import__(m, fromlist=[k])
    klass = getattr(mod, k)

    ProcessWrapper(klass).run()

if __name__ == '__main__':
    main()

