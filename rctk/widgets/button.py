import cgi
from rctk.widgets.control import Control, Attribute

from rctk.task import Task
from rctk.event import Clickable

class Button(Control, Clickable):
    name = "button"

    text = Attribute('', Attribute.STRING, filter=cgi.escape)

    def __init__(self, tk, text, **properties):
        super(Button, self).__init__(tk, text=text, **properties)

