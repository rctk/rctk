#!/usr/bin/env python

from rctk.webpy import serve

def main():
    import sys
    import os

    args = sys.argv
    if len(args) < 2:
        print >> sys.stderr, "Usage: serve_webpy.py module.class"
        sys.exit(-1)
    if '.' not in args[1]:
        print >> sys.stderr, "Usage: serve_webpy.py module.class"
        sys.exit(-1)

    m, k = args[1].rsplit(".", 1)
    mod = __import__(m, fromlist=[k])
    klass = getattr(mod, k)

    ## web.py scans the arguments as well
    del args[1]

    ## so /static works
    os.chdir(os.path.dirname(__file__))

    serve(klass)

if __name__ == '__main__':
    main()

