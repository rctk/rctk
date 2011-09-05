from rctk.widgets.control import Attribute
from rctk.widgets.container import Container

class Panel(Container):
    """ a simple container-control to add elements using 
        a layoutmanager.
    """
    name = "panel"

    scrolling = Attribute(False, Attribute.BOOLEAN)

    ## valid: top, bottom, left, right. Create-only attribute. XXX
    scrollto = Attribute("", Attribute.STRING)

    def scrollbottom(self):
        self.scrollto = "bottom"

    def scrolltop(self):
        self.scrollto = "top"

