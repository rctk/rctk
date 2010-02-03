from control import Control

from rctk.task import Task
from rctk.event import Clickable

class Button(Control, Clickable):
    name = "button"

    def __init__(self, tk, text, **properties):
        super(Button, self).__init__(tk, text=text, **properties)

    properties = Control.extend(text="")
