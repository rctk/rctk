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

    classid = args[1]

    ## web.py scans the arguments as well
    del args[1]

    serve(classid)

if __name__ == '__main__':
    main()

