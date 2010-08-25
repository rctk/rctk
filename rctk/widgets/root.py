from rctk.widgets.control import remote_attribute
from rctk.widgets.container import Container

class Root(Container):
    """ the root window. Unique, id 0 """
    name = "root"

    ## traditional properties don't really work
    ## on the Root control, and they conflict
    ## with remote_attributes with the same name.

    properties = {}

    title = remote_attribute("title", "RCTK")
    width = remote_attribute("width", 0)
    height = remote_attribute("height", 0)


    def __init__(self, tk):
        super(Root, self).__init__(tk)

    @classmethod
    def newid(self):
        """ the root window always has id 0 """
        return 0

    def create(self):
        """ there's no need to create a Root, it's done implicitly.
            In tests we actually assume no root create task is 
            generated """
        pass
