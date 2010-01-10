from control import Control

from rctk.task import Task
from rctk.event import Clickable


class CheckBox(Control, Clickable):
    """Simple CheckBox control. Keyword argument default sets default checked state."""
    name = "checkbox"
    
    def __init__(self, tk, default=False):
        super(CheckBox, self).__init__(tk)
        self._checked = default
        self.tk.queue(Task("CheckBox created id %d checked '%s'" % (self.id, self.checked),
          {'control':self.name, 'id':self.id, 'action':'create', 'defaultChecked':self.checked}))
    
    def sync(self, **data):
        if 'checked' in data:
            self._checked = data['checked']
    
    def _get_checked(self):
        return self._checked
    
    def _set_checked(self, val):
        self._checked = val
        self.tk.queue(Task("CheckBox id %d checked changed to '%s'" % (self.id, self.checked),
          {'control':self.name, 'id':self.id, 'action':'update', 'update':{'checked':self.checked}}))
    
    checked = property(_get_checked, _set_checked)
    
    def toggle(self):
        self.checked = not self.checked
