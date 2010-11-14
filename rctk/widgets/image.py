import os, cgi
from rctk.widgets.control import Control, remote_attribute
from rctk.resourceregistry import addResource, BaseResource, FileResource
from rctk.event import Clickable
from rctk.task import Task

class Image(Control):
    name = 'image'
    
    title = remote_attribute('title', '', lambda self, s: cgi.escape(s))
    
    def __init__(self, tk, resource='', url='', title='', **properties):
        self._resource = resource
        self._url = url
        self._title = title
        super(Image, self).__init__(tk, **properties)
    
    def create(self):
        t = dict(title=cgi.escape(self.title))
        if self._resource:
            t['resource'] = self._resource.name
        if self._url:
            t['url'] = self.url

        self.tk.create_control(self, **t)
        
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

    def get_url(self):
        return self._url
    
    def set_url(self, url):
        self._url = url
        self.tk.queue(Task("%s id %d attr url update to '%s'" % 
            (self.name, self.id, self._url),
            {
                'control':self.name,
                'id':self.id,
                'action':'update',
                'update':{'url':self._url}
            }))
    url = property(get_url, set_url) 

class ImageData(Image):
    def __init__(self, tk, data, name=None, type=None, title='', **properties):
        resource = BaseResource(data, name=name, type=type)
        addResource(resource)
        super(ImageData, self).__init__(tk, resource=resource, title=title, **properties)
    

class ImageFile(Image):
    def __init__(self, tk, path, name=None, type=None, title='', **properties):
        resource = FileResource(path, name=name, type=type)
        addResource(resource)
        super(ImageFile, self).__init__(tk, resource=resource, title=title, **properties)
    
