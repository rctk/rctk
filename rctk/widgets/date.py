from rctk.widgets.control import Control, Attribute

from rctk.task import Task
from rctk.event import Changable

class Date(Control, Changable):
    name = "date"

    value = Attribute("", Attribute.STRING)

    def create(self):
        ## XXX this should become a "real" property!
        self.tk.create_control(self, pickerconfig={'dateFormat':'yy-mm-dd'})

