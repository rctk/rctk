##
## Load and start an application as a standalone process

import sys
import os

import simplejson
from rctk.toolkit import factory
from rctk.util import un_unicode
import cgitb

class ProcessWrapper(object):
    def __init__(self, klass, debug, stdin, stdout):
        self.debug = debug
        self.stdin = stdin
        if self.stdin == sys.stdin:
            sys.stdin = open("/dev/null", "r")
        self.stdout = stdout
        if self.stdout == sys.stdout:
            sys.stdout = open("/dev/null", "w")
        app = klass()
        self.tk = factory(app, debug=debug)
        self.tk.startupdir = os.getcwd() # ??

    def run(self):
        while True:
            # import rpdb2; rpdb2.start_embedded_debugger("foo")
            try:
                size = int(self.stdin.readline().strip())
                message = self.stdin.read(size)
                type, rest = message.split(" ", 1)
                if type == "SERVE":
                    try:
                        type, data = self.tk.serve(rest)
                        result = {'type':type, 'data':data.encode('base64')}
                    except KeyError, e:
                        result = {}
                elif type == "HANDLE":
                    # print rest
                    method, args_str = rest.split(" ", 1)
                    ## make sure we're not passing unicode keys as keyword
                    ## arguments
                    args = un_unicode(simplejson.loads(args_str))
                    result = self.tk.handle(method, **args)
                else:
                    ## wtf?
                    pass

                message = simplejson.dumps(result)
            except Exception, e:
                message = "ERROR " + simplejson.dumps({'html':cgitb.html(sys.exc_info()), 'text':cgitb.text(sys.exc_info())})

            self.stdout.write("%d\n%s" % (len(message), message))
            self.stdout.flush()
                
def main():
    # preserve original sys.stdin/sys.stdout and redirect them to something safe.
    debug = False
    stdin = sys.stdin
    sys.stdin = open("/dev/null", "r")
    stdout = sys.stdout
    sys.stdout = sys.stderr = open("/tmp/out.txt", "w")

    ## order is relevant, for now. ugh
    if sys.argv[1].startswith("--startupdir="):
        startupdir = sys.argv[1][13:]
        os.chdir(startupdir)
        del sys.argv[1]
    if sys.argv[1] == "--debug":
        debug = True
        del sys.argv[1]
    appid = sys.argv[1]
    m, k = appid.rsplit('.', 1)
    mod = __import__(m, globals(), locals(), [k])
    klass = getattr(mod, k)

    ProcessWrapper(klass, debug, stdin, stdout).run()

if __name__ == '__main__':
    main()

