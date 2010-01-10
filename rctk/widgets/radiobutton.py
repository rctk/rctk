from rctk.event import Clickable
from rctk.task import Task

from control import Control, remote_attribute

class RadioButton(Control, Clickable):
    name = "radiobutton"
    
    group = remote_attribute('group', '')
    value = remote_attribute('value', '')
    checked = remote_attribute('checked', False)
    
    def __init__(self, tk, group="", default=False, value=""):
        super(RadioButton, self).__init__(tk)
        self._group = group
        self._value = value
        self._checked = default
        self.tk.queue(Task(
            "RadioButton created id %d, group %s, value %s, checked %s" % (self.id,
              self.group, self.value, self.checked),
            {
                'control':self.name,
                'id':self.id,
                'action':'create',
                'name':self.group,
                'value':self.value,
                'defaultChecked':self.checked,
            }
        ))

    def sync(self, **data):
        if 'checked' in data:
            self._checked = data['checked']
    
    def toggle(self):
        self.checked = not self.checked

class RadioButtonGroup(Control):
    name = "radiobuttongroup"

    def add(self, button):
        button.group = "ctrl" + str(self.id)
    
