import os, cgi
from rctk.widgets.control import Control, remote_attribute
from rctk.resourceregistry import addResource, ImgFileResource
from rctk.event import Clickable

class Image(Control):
    name = "image"
    
    title = remote_attribute("title", "", lambda self, s: cgi.escape(s))
    
    def __init__(self, tk, data, title="", name=None, type=None, **properties):
        self._resource = ImgResource(data, name=name, type=type)
        self._title = title
        addResource(self._resource)
        super(Image, self).__init__(tk, **properties)
    
    def create(self):
        self.tk.create_control(self, resource=self._resource.name, title=cgi.escape(self.title))
    

class ImageFile(Image):
    def __init__(self, tk, path, title="", type=None, **properties):
        self._resource = ImgFileResource(path, type=type)
        self._title = title
        addResource(self._resource)
        super(Image, self).__init__(tk, **properties)

    
class ImageResource(Image):
    def __init__(self, tk, resource, title="", **properties):
        self._resource = resource
        self._title = title
        super(Image, self).__init__(tk, **properties)
    

