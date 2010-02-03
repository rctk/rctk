from rctk.task import Task
from container import Container

class Panel(Container):
    """ a simple container-control to add elements using 
        a layoutmanager.
    """
    name = "panel"

    properties = Container.extend(scrolling=False)

