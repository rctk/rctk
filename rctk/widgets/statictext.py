from control import Control

from rctk.task import Task
from rctk.event import Clickable


class StaticText(Control):
    name = "statictext"

    properties = Control.extend(wrap=False)

    def __init__(self, tk, text, **options):
        self._text = text
        super(StaticText, self).__init__(tk, **options)

    def create(self):
        self.tk.create_control(self, text=self.text)

    def _get_text(self):
        return self._text

    def _set_text(self, text):
        self._text = text
        self.tk.queue(Task("StaticText update id %d text '%s'" % (self.id, self._text),
          {'control':self.name, 'id':self.id, 'action':'update', "update":{"text":self.text}}))

    text = property(_get_text, _set_text)
