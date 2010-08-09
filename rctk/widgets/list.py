from rctk.widgets.control import remote_attribute
from rctk.widgets.dropdown import Dropdown
from rctk.task import Task

class List(Dropdown): # confusing name - list vs List?
    name = "list"
    """
        A list is functionally the same as a Dropdown, it's just rendered
        differently and it can display a number of items at once.
    """
    size = remote_attribute('size', 0)
    _size = 0

    def __init__(self, tk, items=(), size=5, multiple=False):
        self._size = size
        super(List, self).__init__(tk, items, multiple)

    def create(self):
        self.tk.create_control(self, items=self._items(), size=self._size, multiple=self._multiple)
