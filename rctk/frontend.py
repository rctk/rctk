from rctk.util import resolveclass
from rctk.resourceregistry import getResourceRegistry

class Frontend(object):
    def __init__(self, tk):
        self.rr = getResourceRegistry()
        self.tk = tk

    @classmethod
    def workingdir(cls):
        return "."

    @classmethod
    def serve_resource(cls, name):
        # name starts with resource/
        elements = name.split('/')
        resource = getResourceRegistry().get_resource(elements[1], elements)
        return (resource.type, resource.data)

    @classmethod
    def index_html(self):
        return "No frontend loaded"

class Loader(object):
    @classmethod
    def load(cls, name):
        return resolveclass(name)

class Registry(object):
    frontends = []

    @classmethod
    def register(cls, name, frontend):
        cls.frontends.append((name, frontend))

    @classmethod
    def get(cls, name):
        for fname, frontend in cls.frontends:
            if fname == name:
                return frontend
        return None
