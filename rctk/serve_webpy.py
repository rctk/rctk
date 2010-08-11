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

    session_class = Session

    classid = ''
    use_cookies = False
    debug = False

    while not classid:
        if args[1] in('--use_cookies', '--use-cookies'):
            use_cookies = True
        if args[1] == '--debug':
            debug = True
        elif args[1] in ('--spawned_sessions', '--spawned-sessions'):
            session_class = SpawnedSession
        else:
            classid = args[1]
        ## web.py scans the arguments as well
        del args[1]

    if not classid or '.' not in classid:
        print >> sys.stderr, usage
        sys.exit(-1)

    cwd = os.getcwd()
    manager = Manager(session_class, classid, cwd, debug=debug)
    serve(manager, use_cookies=use_cookies)

if __name__ == '__main__':
    main()

