from rctk.widgets.control import Control, Attribute

from rctk.event import Clickable


class RadioButton(Control, Clickable):
    """Simple Radiobutton control."""
    name = "radiobutton"

    checked = Attribute(False, Attribute.BOOLEAN)
    text = Attribute(False, Attribute.BOOLEAN)
    group = Attribute("", Attribute.STRING)

    def __init__(self, tk, value=None, **properties):
        self.value = value
        self._group = None
        super(RadioButton, self).__init__(tk, **properties)

    def __repr__(self):
        return '<%s name="%s" id=%d checked=%s>' % (self.__class__.__name__, self.name, self.id, self.checked)

    def sync(self, **attributes):
        """ intercept updates to "check", make sure other radiobuttons
            are no longer checked """
        if self._group and "checked" in attributes:
            if attributes["checked"]:
                self._group.checked(self)

        return super(RadioButton, self).sync(**attributes)
        
class RadioGroup(Clickable):
    name = "radiogroup"
    counter = 0

    def __init__(self, *buttons):
        self._radios = []
        self.groupid = "group%d" % self.counter
        RadioGroup.counter += 1

        super(RadioGroup, self).__init__()

        for b in buttons:
            self.add(b)

    def create(self):
        # we don't actually create a group control at the Onion side
        pass

    def checked(self, radio):
        """ radiobutton 'radio' notifies the group it has been checked
            Reset the checked state on all other radios """
        for b in self._radios:
            if b != radio:
                b.sync(checked=False)

    def add(self, b):
        if b not in self._radios:
            self._radios.append(b)
            b.group = self.groupid
            b.click = self.handle_radiobutton
            b._group = self

    def handle_radiobutton(self, e):
        if self._click_handler:
            self._click_handler(e)

    def _get_value(self):
        for b in self._radios:
            if b.checked:
                return b.value
        return None

    def _set_value(self, v):
        for b in self._radios:
            if b.value == v:
                b.checked = True

    value = property(_get_value, _set_value)

    def _get_selected(self):
        for b in self._radios:
            if b.checked:
                return b
        return None

    def _set_selected(self, b):
        if b in self._radios:
            b.checked = True
        else:
            raise KeyError("Control %s not part of group" % b.id)

    selected = property(_get_selected, _set_selected)

    ##
    ## Don't use default implementation - avoid sending tasks
    def _get_click(self):
        return self._click_handler

    def _set_click(self, val):
        self._click_handler = val
        for b in self._radios:
            if not b.click:
                b.click = val

    click = property(_get_click, _set_click)

from rctk.widgets.panel import Panel
    
class RadioPanel(Panel, RadioGroup):
    """
        Added controls are automatically part of/handled by the group
    """
    name = "radiopanel"
