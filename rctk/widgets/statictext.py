from control import Control, remote_attribute

from rctk.task import Task
from rctk.event import Clickable

import cgi


class StaticText(Control):
    name = "statictext"

    ## size (fontsize), family
    ## decoration can be underline, overstrike
    properties = Control.extend(
                     wrap=False, 
                     bold=False, 
                     italic=False,
                     decoration="")

    def __init__(self, tk, text, **options):
        self._text = text
        super(StaticText, self).__init__(tk, **options)

    def create(self):
        self.tk.create_control(self, text=self._escape(self.text))

    def _escape(self, s):
        """ perform filtering/escaping if necessary """
        return cgi.escape(s)

    text = remote_attribute("text", "", _escape)
    #def _get_text(self):
    #    return self._text

    #def _set_text(self, text):
    #    self._text = text
    #    self.tk.queue(Task("StaticText update id %d text '%s'" % (self.id, self._text),
    #      {'control':self.name, 'id':self.id, 'action':'update', "update":{"text":self._escape(self.text)}}))

    #text = property(_get_text, _set_text)

class StaticHTMLText(StaticText):
    def _escape(self, s):
        """ for now, allow any html/css/javascript to pass through. But eventually, this
            should be an explicit option and only a small subset of html should be allowed
            by default
        """
        return s

