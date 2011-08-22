from rctk.widgets.control import Control, Attribute

from rctk.event import Clickable

class CheckBox(Control, Clickable):
    """Simple CheckBox control."""
    name = "checkbox"

    checked = Attribute(False, Attribute.BOOLEAN)
    text = Attribute(False, Attribute.STRING)

    def __init__(self, tk, **properties):
        super(CheckBox, self).__init__(tk, **properties)

    def toggle(self):
        self.checked = not self.checked

    def __repr__(self):
        return '<%s name="%s" id=%d checked=%s>' % (self.__class__.__name__, self.name, self.id, self.checked)


