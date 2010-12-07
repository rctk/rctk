from rctk.widgets.control import Control, Attribute

from rctk.task import Task
from rctk.event import Changable, Submittable, Keypressable

class Text(Control, Changable, Submittable, Keypressable):
    name = "text"

    value = Attribute("")
    rows = Attribute(1, Attribute.NUMBER)
    columns = Attribute(20, Attribute.NUMBER)

class Password(Text):
    name = "password"
