from rctk.task import Task
from rctk.widgets.container import Container


class Window(Container):
    name = "window"

    properties = Container.extend(title="Window", modal=False)

    def __init__(self, tk, title, **properties):
        super(Window, self).__init__(tk, title=title, **properties)

    ## keep track of state (open/closed), both ways! So not just methods to open/close remotely

    ## allow title to be updated
    def open(self):
        self.tk.queue(Task("Window id %d opened" % self.id,
          {'control':self.name, 'id':self.id, 'action':'update', "update":{'state':'open'}}))

    def close(self):
        self.tk.queue(Task("Window id %d closed" % self.id,
          {'control':self.name, 'id':self.id, 'action':'update', "update":{'state':'close'}}))
