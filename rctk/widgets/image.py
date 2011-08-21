import cgi
from rctk.widgets.control import Control, Attribute
from rctk.resourceregistry import addResource, BaseResource, FileResource
from rctk.event import Clickable
from rctk.task import Task

class Image(Control):
    name = 'image'

    title = Attribute('', filter=cgi.escape)
    url = Attribute('')
    resource = Attribute('')

    def __init__(self, tk, resource='', url='', title='', **properties):
        super(Image, self).__init__(tk, title=title, url=url, 
                                    resource=resource, **properties)

class ImageData(Image):
    def __init__(self, tk, data, name=None, type=None, title='', 
                 **properties):
        resource = BaseResource(data, name=name, type=type)
        resourcename = addResource(resource)
        super(ImageData, self).__init__(tk, resource=resourcename, 
                                        title=title, **properties)

class ImageFile(Image):
    def __init__(self, tk, path, name=None, type=None, title='', 
                 **properties):
        resource = FileResource(path, name=name, type=type)
        resourcename = addResource(resource)
        
        super(ImageFile, self).__init__(tk, resource=resourcename, 
                                        title=title, **properties)

