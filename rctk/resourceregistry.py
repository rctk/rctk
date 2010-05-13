import os
import sys

from rctk.util import OrderedDict

class BaseResource(object):
    def __init__(self, path, name=None):
        if name is None:
            self.name = os.path.basename(path)
        else:
            self.name = name
        ## some magic to allow paths relative to calling module
        frame = sys._getframe(1)
        base = os.path.dirname(frame.f_globals['__file__'])
        if path.startswith('/'):
            self.path = path
        else:
            self.path = os.path.join(base, path)
        self.data = open(self.path, "r").read()

    def __repr__(self):
        return '<%s name="%s" path="%s">' % (self.__class__.__name__, self.name, self.path)
class JSResource(BaseResource):
    pass

class CSSResource(BaseResource):
    pass

class ResourceRegistry(object):
    """ The resource registry is used to register javascript and
        css that is used by rctk. It allows the main page to be
        built dynamically and allows certain optimizations such as

        - merging
        - compression
        - caching
        - keep resources local to the code
        - possibility to render inline

        Currently, the ResourceRegistry can't properly handle @import in css.
        It would probably need to load and merge these imports itself, or load
        the imported css into the registry itself, possibly renaming the css in
        the process.

        At this point, this is only an issue with jqueryui, which we'll keep as a static
        dependency for now.
    """
    def __init__(self):
        self.resources = OrderedDict()

    def add(self, resource):
        name = resource.name
        counter = 1
        while name in self.resources:
            name = "%s%d" % (resource.name, counter)
            counter += 1
        self.resources[name] = resource

    def css_resources(self):
        """ return references to css resources. They may be merged so it
            may be just a single resource """
        return [k for (k,v) in self.resources.iteritems() if isinstance(v, CSSResource)]

    def js_resources(self):
        """ return references to css resources. They may be merged so it
            may be just a single resource """
        return [k for (k,v) in self.resources.iteritems() if isinstance(v, JSResource)]

    def get_resource(self, name):
        """ return a (type, data) tuple containing the mimetype and resource data """
        r = self.resources[name]
        type = 'application/data'
        if isinstance(r, CSSResource):
            type = 'text/css'
        elif isinstance(r, JSResource):
            type = 'text/javascript'
        return (type, r.data)

    def header(self):
        """ return html usable for injection into <head></head> """
        res = []
        for css in self.css_resources():
            res.append('<link type="text/css" href="resources/%s" rel="stylesheet" />' % css)
        for js in self.js_resources():
            res.append('<script type="text/javascript" src="resources/%s"></script>' % js)

        return '<!-- dynamic resources -->\n%s\n<!-- end dynamic resources -->' % '\n'.join(res)

_instance = None

def getResourceRegistry():
    """ singleton-ish """
    global _instance
    if _instance is None:
        _instance = ResourceRegistry()
    return _instance

def addResource(r):
    getResourceRegistry().add(r)

