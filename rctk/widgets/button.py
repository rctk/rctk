from control import Control

from rctk.task import Task
from rctk.event import Clickable

class Button(Control, Clickable):
    name = "button"
    def __init__(self, tk, text):
        super(Button, self).__init__(tk)
        self.text = text
        self.tk.queue(Task("Button created id %d text '%s'" % (self.id, self.text),
         {'control':self.name, "id":self.id, "action":"create", "text":self.text}))
