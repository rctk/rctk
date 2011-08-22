from rctk.widgets.control import Control, Attribute

from rctk.task import Task
from rctk.event import Clickable


class RadioButton(Control, Clickable):
    """Simple Radiobutton control."""
    name = "checkbox"

    checked = Attribute(False, Attribute.BOOLEAN)

    def __init__(self, tk, value=None, group=None, **properties):
        ## value and group are used by Radiobutton
        self.value = value
        self._group = group
        super(RadioButton, self).__init__(tk, **properties)
        if group:
            group.add(self)

    def create(self):
        groupid = None
        if self._group:
            groupid = self._group.id
        self.tk.create_control(self, group=groupid, defaultChecked=self.checked)

    def toggle(self):
        self.checked = not self.checked

    def __repr__(self):
        return '<%s name="%s" id=%d checked=%s>' % (self.__class__.__name__, self.name, self.id, self.checked)


class RadioGroup(Control, Clickable):
    ## currently broken, see issue:31
    name = "checkboxgroup"

    def __init__(self, tk, **properties):
        self._boxes = []
        self._checked = None
        super(RadioGroup, self).__init__(tk)

    def create(self):
        # we don't actually create a group control at the Onion side
        pass

    def add(self, b):
        if b not in self._boxes:
            self._boxes.append(b)
            if self._click_handler and not b.click:
                b.click = self._click_handler
            if b.checked:
                self._checked = b 

    def _get_value(self):
        for b in self._boxes:
            if b.checked:
                return b.value
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
    
