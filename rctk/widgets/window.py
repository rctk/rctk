from rctk.widgets.control import Attribute
from rctk.widgets.container import Container
from rctk.event import Closable

class Window(Container, Closable):
    name = "window"

    containable = False

    title = Attribute("Window", Attribute.STRING)
    modal = Attribute(False, Attribute.BOOLEAN)
    resizable = Attribute(False, Attribute.BOOLEAN)
    position = Attribute("top", Attribute.STRING) # can also be (x,y)
    opened = Attribute(False, Attribute.BOOLEAN)

    def __init__(self, tk, title="", **properties):
        super(Window, self).__init__(tk, title=title, **properties)

    def open(self):
        self.opened = True

    def shut(self):
        self.opened = False
