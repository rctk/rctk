#!/usr/bin/env python

from rctk.webpy import serve
from rctk.sessions import Session, SpawnedSession, Manager

def main():
    import sys
    import os

    usage = "Usage: serve_webpy.py [--use_cookies] [--spawned_sessions] module.class"

    args = sys.argv
    if len(args) < 2:
        print >> sys.stderr, usage
        sys.exit(-1)
    #if '.' not in args[1]:
    #    print >> sys.stderr, usage
    #    sys.exit(-1)

    classid = ''
    use_cookies = False
    spawned_sessions = False

    while not classid:
        if args[1] == '--use_cookies':
            use_cookies = True
        elif args[1] == '--spawned_sessions':
            spawned_sessions = True
        else:
            classid = args[1]
        ## web.py scans the arguments as well
        del args[1]

    cwd = os.getcwd()
    manager = Manager(Session, classid, cwd)
    if spawned_sessions:
        manager = Manager(SpawnedSession, classid, cwd)
    serve(manager, use_cookies=use_cookies)

if __name__ == '__main__':
    main()

