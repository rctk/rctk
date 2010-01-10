from rctk.task import Task
from container import Container


class Window(Container):
    name = "window"

    def __init__(self, tk, title, modal=False):
        super(Window, self).__init__(tk)
        self.title = title
        self.tk.queue(Task("Window created id %d title '%s'" % (self.id, self.title),
          {'control':self.name, 'id':self.id, 'action':'create', "title":self.title, 'modal':modal}))

    ## keep track of state (open/closed), both ways! So not just methods to open/close remotely

    ## allow title to be updated
    def open(self):
        self.tk.queue(Task("Window id %d opened" % self.id,
          {'control':self.name, 'id':self.id, 'action':'update', "update":{'state':'open'}}))

    def close(self):
        self.tk.queue(Task("Window id %d closed" % self.id,
          {'control':self.name, 'id':self.id, 'action':'update', "update":{'state':'close'}}))
