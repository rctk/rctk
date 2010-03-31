import cgi
from control import Control

from rctk.task import Task
from rctk.event import Clickable

class Button(Control, Clickable):
    name = "button"

    def __init__(self, tk, text, **properties):
        self._text = text
        super(Button, self).__init__(tk, **properties)

    def create(self):
        self.tk.create_control(self, text=cgi.escape(self.text))

    def _get_text(self):
        return self._text

    def _set_text(self, text):
        self._text = text
        self.tk.queue(Task("Button update id %d test '%s'" % (self.id, self._text), {'control':self.name, 'id':self.id, 'action':"update", "update":{"text":cgi.escape(self.text)}}))

    text = property(_get_text, _set_text)

