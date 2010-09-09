#!/usr/bin/python

from rctk.sessions import Session, SpawnedSession, Manager
from rctk.webpy import app
import os

startupdir = os.getcwd()
manager = None

def application(environ, start_response):
    global manager
    use_cookies = environ.get('rctk.use_cookies', "false").lower() in ("1", "true")
    if manager is None:
        classid = environ.get('rctk.classid')
        debug = environ.get('rctk.debug', "false").lower() in ("1", "true")
        session = environ.get('rctk.session')
        
        options = {}

        optionconfig = environ.get('options')
        if optionconfig:
            for kv in optionconfig.split(','):
                k, v = kv.split("=", 1)
                options[k] = v
            
        if session == "SpawnedSession":
            sessionclass = SpawnedSession
        else:
            sessionclass = Session

        manager = Manager(SpawnedSession, classid, startupdir, debug, **options)
    return app(manager, use_cookies).wsgifunc()(environ, start_response)

