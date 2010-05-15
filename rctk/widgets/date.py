from rctk.widgets.control import Control

from rctk.task import Task
from rctk.event import Changable

class Date(Control, Changable):
    name = "date"

    def __init__(self, tk, **properties):
        super(Date, self).__init__(tk, **properties)
        self._value = ""

    def create(self):
        ## XXX this should become a "real" property!
        self.tk.create_control(self, pickerconfig={'dateFormat':'yy-mm-dd'})

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value
        self.tk.queue(Task("Date id %d value changed to '%s'" % (self.id, value),
         {'control':self.name, "id":self.id, "action":"update", "update":{'value':value}}))

    value = property(_get_value, _set_value)

    def sync(self, **data):
        if 'value' in data:
            self._value = data['value']
