from rctk.widgets.control import Attribute
from rctk.widgets.container import Container

class Root(Container):
    """ the root window. Unique, id 0 """
    name = "root"

    containable = False

    title = Attribute("RCTK")
    width = Attribute(0, Attribute.NUMBER)
    height = Attribute(0, Attribute.NUMBER)


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
