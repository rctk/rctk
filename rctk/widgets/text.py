from control import Control

from rctk.task import Task
from rctk.event import Changable

class Text(Control, Changable):
    name = "text"

    def __init__(self, tk):
        self._value = ""
        super(Text, self).__init__(tk)

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value
        self.tk.queue(Task("Text id %d value changed to '%s'" % (self.id, value),
         {'control':self.name, "id":self.id, "action":"update", "update":{'value':value}}))

    value = property(_get_value, _set_value)

    def sync(self, **data):
        if 'value' in data:
            self._value = data['value']
