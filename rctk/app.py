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
    """
    debug = False
    polling = 0

    def __init__(self):
        pass

    def create_toolkit(self, **kw):
        debug = kw.get('debug', self.debug)
        polling = kw.get('polling', self.polling)

        self.tk = Toolkit(self, debug, polling)
        return tk

    @classmethod
    def create(cls):
        a = cls()
        a.create_toolkit()
        return a

    def run(self, tk):
        pass

def factory(appid, **config):
    o = resolveclass(appid)
    ## handle defaults
    debug = config.get('debug', False)
    polling = config.get('polling', 0)
    if not callable(o):
        raise AppNotCallable(appid)
    if not implements(o, App):
        # old style or just plain wrong 
        print >> sys.stderr, "Deprecation Warning: Please subclass rctk.app.App"
        a = o(*args, **kw)
        tk = Toolkit(a, debug=debug, polling=polling) # ???
        return a
    else:
        a = App()
        a.create()
        a.create_toolkit(debug=debug, polling=polling)



