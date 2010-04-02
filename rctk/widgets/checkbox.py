from control import Control, remote_attribute

from rctk.task import Task
from rctk.event import Clickable


class CheckBox(Control, Clickable):
    """Simple CheckBox control."""
    name = "checkbox"
    
    checked = remote_attribute('checked', False)
    
    def __init__(self, tk, value=None, group=None, checked=False, **properties):
        self.value = value
        self._group = group
        self._checked = checked
        super(CheckBox, self).__init__(tk, **properties)
        if group:
            group.add(self)
    
    def create(self):
        groupid = None
        if self._group:
            groupid = self._group.id
        self.tk.create_control(self, group=groupid, defaultChecked=self.checked)
    
    def sync(self, **data):
        if 'checked' in data:
            self._checked = data['checked']
    
    def toggle(self):
        self.checked = not self.checked
    
    def __repr__(self):
        return '<%s name="%s" id=%d checked=%s>' % (self.__class__.__name__, self.name, self.id, self.checked)
    

class CheckBoxGroup(Control, Clickable):
    name = "checkboxgroup"

    def __init__(self, tk, **properties):
        self._boxes = []
        self._checked = None
        super(CheckBoxGroup, self).__init__(tk)
    
    def create(self):
        # we don't actually create a group control at the Onion side
        pass

    def add(self, b):
        if not b in self._boxes:
            self._boxes.append(b)
            if self._click_handler and not b.click:
                b.click = self._click_handler
            if b.checked:
                self._checked = b 

    def _get_value(self):
        if self._checked:
            return self._checked.value
        return None

    def _set_value(self, v):
        for b in self._boxes:
            if b.value == v:
                b.checked = true

    value = property(_get_value, _set_value)
    
    def _get_click(self):
        return self._click_handler
    
    def _set_click(self, val):
        self._click_handler = val
        for b in self._boxes:
            if not b.click:
                b.click = val
    
    click = property(_get_click, _set_click)
    
