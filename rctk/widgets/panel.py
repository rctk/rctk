from rctk.task import Task
from rctk.widgets.control import Attribute
from rctk.widgets.container import Container

class Panel(Container):
    """ a simple container-control to add elements using 
        a layoutmanager.
    """
    name = "panel"

    scrolling = Attribute(False, Attribute.BOOLEAN)

