from rctk.util import resolveclass

class Frontend(object):
    def init(self, tk):
        pass

    @classmethod
    def workingdir(cls):
        return "."

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
