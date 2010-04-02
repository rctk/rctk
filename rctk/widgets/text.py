from control import Control, remote_attribute

from rctk.task import Task
from rctk.event import Changable, Submittable

class Text(Control, Changable, Submittable):
    name = "text"

    value = remote_attribute('value', "")

    def __init__(self, tk, value=""):
        self._value = value
        super(Text, self).__init__(tk)
        
    def create(self):
        self.tk.create_control(self, value=self._value)

    def sync(self, **data):
        if 'value' in data:
            self._value = data['value']
    

class Password(Text):
    name = "password"
