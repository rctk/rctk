import cgi
from rctk.widgets.control import Control, remote_attribute

from rctk.task import Task
from rctk.event import Clickable

class Image(Control):
    name = "image"

    src = remote_attribute("src", "")
    title = remote_attribute("title", "", lambda self, s: cgi.escape(s))

    def __init__(self, tk, src, title="", **properties):
        self._src = src
        self._title = title
        super(Image, self).__init__(tk, **properties)

    def create(self):
        self.tk.create_control(self, src=self.src, title=cgi.escape(self.title))
    
