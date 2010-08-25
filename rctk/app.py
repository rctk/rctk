from rctk.toolkit import Toolkit
from rctk.util import resolveclass


class AppException(Exception):
    pass

class AppNotCallable(AppException):
    """ The application is not callable. I.e. it's not a class """
    pass

class AppNotRunnable(AppException):
    """ The application does not have a run() method """
    pass

class App(object):
    """
        Base class for rctk apps.

        Not sure if we really, really need this.
    """
    debug = False
    polling = 0

    def __init__(self):
        pass

    def run(self, tk):
        pass

import warnings

def check_classid(classid):
    o = resolveclass(classid)
    if not callable(o):
        raise AppNotCallable(classid)
    if not issubclass(o, App):
        # old style or just plain wrong 
        warnings.warn("Deprecation Warning: Please subclass rctk.app.App", DeprecationWarning)
        
