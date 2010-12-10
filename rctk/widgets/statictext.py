from rctk.widgets.control import Control, Attribute

from rctk.task import Task
from rctk.event import Clickable

import cgi


class StaticText(Control):
    name = "statictext"

    ## size (fontsize), family
    ## decoration can be underline, overstrike
    text = Attribute()
    wrap = Attribute(False, Attribute.BOOLEAN)
    bold = Attribute(False, Attribute.BOOLEAN)
    italic = Attribute(False, Attribute.BOOLEAN)
    decoration = Attribute()

    def __init__(self, tk, text="", **attrs):
        super(StaticText, self).__init__(tk, text=text, **attrs)

def html_escape(s):
    """ for now, allow any html/css/javascript to pass through. But eventually,
        this should be an explicit option and only a small subset of html
        should be allowed by default
    """
    return s

from rctk.event import Clickable

class StaticHTMLText(StaticText, Clickable):
    name = "statichtmltext"

    text = Attribute(filter=html_escape)

