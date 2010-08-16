import os, cgi
from rctk.widgets.control import Control, remote_attribute
from rctk.resourceregistry import addResource, BaseResource, FileResource
from rctk.event import Clickable
from rctk.task import Task

class Image(Control):
    name = 'image'
    
    title = remote_attribute('title', '', lambda self, s: cgi.escape(s))
    
    def __init__(self, tk, resource, title='', **properties):
        self._resource = resource
        self._title = title
        super(Image, self).__init__(tk, **properties)
    
    def create(self):
        self.tk.create_control(self, resource=self._resource.name, title=cgi.escape(self.title))
        
    def get_resource(self):
        return self._resource
    
    def set_resource(self, resource):
        self._resource = resource
        self.tk.queue(Task("%s id %d attr resource update to '%s'" % 
            (self.name, self.id, self._resource.name),
            {
                'control':self.name,
                'id':self.id,
                'action':'update',
                'update':{'resource':self._resource.name}
            }))
    resource = property(get_resource, set_resource) 

class ImageData(Image):
    def __init__(self, tk, data, name=None, type=None, title='', **properties):
        resource = BaseResource(data, name=name, type=type)
        addResource(resource)
        super(ImageDate, self).__init__(tk, resource, title=title, **properties)
    

class ImageFile(Image):
    def __init__(self, tk, path, name=None, type=None, title='', **properties):
        resource = FileResource(path, name=name, type=type)
        addResource(resource)
        super(ImageFile, self).__init__(tk, resource, title=title, **properties)
    
