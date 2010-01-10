from rctk.task import Task
from container import Container

class Panel(Container):
    """ a simple container-control to add elements using 
        a layoutmanager.
    """
    name = "panel"

    SCROLL_NONE = 0
    SCROLL_HORIZONTAL = 1
    SCROLL_VERTICAL = 2
    SCROLL_AUTO = 4
    SCROLL_BOTH = SCROLL_HORIZONTAL | SCROLL_VERTICAL

    def __init__(self, tk, scrolling=False):
        super(Panel, self).__init__(tk)
        self.scrolling = scrolling
        self.tk.queue(Task("Panel created id %d" % (self.id, ),
          {'control':self.name, 'id':self.id, 'action':'create', 'scrolling':self.scrolling}))
