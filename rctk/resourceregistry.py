import os
import stat
import sys
import time
import mimetypes

from rctk.compat import OrderedDict

class BaseResource(object):
    type = "application/data"

    counter = 0
    def __init__(self, data, name=None, type=None, timestamp=None):
        self.data = data
        if type is not None:
            self.type = type

        self.timestamp = timestamp or time.time()
        self.name = name
        if self.name is None:
            self.name = "resource%d" % BaseResource.counter
            BaseResource.counter += 1 ## class attribute!

    def __eq__(self, other):
        ## what if timestamp differs?
        return self.data == other.data and self.type == other.type

    def __repr__(self):
        return '<%s name="%s" type="%s" ts="%s" len=%d bytes>' % \
               (self.__class__.__name__, self.name, self.type, self.timestamp, 
                len(self.data))

class FileResource(BaseResource):
    def __init__(self, path, name=None, type=None):
        if name is None:
            name = os.path.basename(path)
        
        ## some magic to allow paths relative to calling module
        if path.startswith('/'):
            self.path = path
        else:
            frame = sys._getframe(1)
            base = os.path.dirname(frame.f_globals['__file__'])
            self.path = os.path.join(base, path)
        if type is None:
            type, encoding = mimetypes.guess_type(self.path)
        data = open(self.path, "r").read()
        timestamp = os.stat(self.path)[stat.ST_MTIME]

        super(FileResource, self).__init__(data, name, type, timestamp)

    def __eq__(self, other):
        if isinstance(other, FileResource):
            ## again, what about timestamp? or name?
            return self.path == other.path

        return False

    def __repr__(self):
        return '<%s name="%s" type="%s" ts="%s" path="%s">' % \
               (self.__class__.__name__, self.name, self.type, self.timestamp, 
                self.path)

class JSResource(BaseResource):
    type = "text/javascript"

class CSSResource(BaseResource):
    type = "text/css"

class JSFileResource(FileResource):
    type = "text/javascript"

class CSSFileResource(FileResource):
    type = "text/css"

class DynamicResource(BaseResource):
    def __call__(self, path):
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

        At this point, this is only an issue with jqueryui, which we'll keep 
        as a static dependency for now.
    """
    def __init__(self):
        self.resources = OrderedDict()

    def add(self, resource):
        ## avoid duplicates
        if resource in self.resources.values():
            return None

        name = resource.name
        counter = 1
        while name in self.resources:
            name = "%s%d" % (resource.name, counter)
            counter += 1
        self.resources[name] = resource
        return name

    ##
    ## (also) provide a way to filter on mimetype, allow matching against
    ## image/* as well.
    def names(self):
        return self.resources.keys()

    def css_resources(self):
        """ return references to css resources. They may be merged so it
            may be just a single resource """
        return [k for (k,v) in self.resources.items() 
                if isinstance(v, (CSSFileResource, CSSResource))]

    def js_resources(self):
        """ return references to css resources. They may be merged so it
            may be just a single resource """
        return [k for (k,v) in self.resources.items() 
                if isinstance(v, (JSFileResource, JSResource))]

    def get_resource(self, name, elements=[]):
        """ 
            return a (type, data) tuple containing the mimetype and resource 
            data 
        """
        r = self.resources[name]

        if isinstance(r, DynamicResource):
            r = r(elements)
        return r

    def header(self):
        """ return html usable for injection into <head></head> """
        res = []
        for css in self.css_resources():
            res.append('<link type="text/css" href="resources/%s"'
                       'rel="stylesheet" />' % css)
        for js in self.js_resources():
            res.append('<script type="text/javascript"'
                       'src="resources/%s"></script>' % js)

        return '<!-- dynamic resources -->\n%s\n<!-- end dynamic resources -->' % '\n'.join(res)

_instance = None

def getResourceRegistry():
    """ singleton-ish """
    global _instance
    if _instance is None:
        _instance = ResourceRegistry()
        mimetypes.init()
    return _instance

def addResource(r):
    getResourceRegistry().add(r)

