from rctk.widgets.control import Attribute
from rctk.widgets.dropdown import Dropdown
from rctk.task import Task

class List(Dropdown): # confusing name - list vs List?
    name = "list"
    """
        A list is functionally the same as a Dropdown, it's just rendered
        differently and it can display a number of items at once.
    """
    size = Attribute(0, Attribute.NUMBER)

