from rctk.task import Task
from rctk.widgets.control import Attribute
from rctk.widgets.container import Container


class Window(Container):
    name = "window"

    containable = False

    title = Attribute("Window", Attribute.STRING)
    modal = Attribute(False, Attribute.BOOLEAN)
    position = Attribute("top", Attribute.STRING) # can also be (x,y)
    ## keep track of state (open/closed), both ways! So not just methods to open/close remotely

    def __init__(self, tk, title="", **properties):
        super(Window, self).__init__(tk, title=title, **properties)


    ## allow title to be updated
    def open(self):
        self.tk.queue(Task("Window id %d opened" % self.id,
          {'control':self.name, 'id':self.id, 'action':'update', "update":{'state':'open'}}))

    def close(self):
        self.tk.queue(Task("Window id %d closed" % self.id,
          {'control':self.name, 'id':self.id, 'action':'update', "update":{'state':'close'}}))
