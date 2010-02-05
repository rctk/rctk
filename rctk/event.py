from rctk.task import Task

class Event(object):
    def __init__(self, control):
        self.control = control

class ClickEvent(Event):
    pass

class ChangeEvent(Event):
    pass

class SubmitEvent(Event):
    pass

class Clickable(object):
    _click_handler = None

    def _set_click(self, val):
        self._click_handler = val
        self.tk.queue(Task("Handler installed on %s %d" % (self.name, self.id),
          {'control':self.name, "id":self.id, "action":"handler", "type":"click"}))

    def _get_click(self):
        return self._click_handler

    click = property(_get_click, _set_click)    

class Changable(object):
    _change_handler = None


    def _set_change(self, val):
        self._change_handler = val
        self.tk.queue(Task("Handler installed on %s %d" % (self.name, self.id),
          {'control':self.name, "id":self.id, "action":"handler", "type":"change"}))

    def _get_change(self):
        return self._change_handler

    change = property(_get_change, _set_change)    

class Submittable(object):
    """ handler to catch explicit submit actions on controls. I.e.
        pressing enter on a Text input. This to avoid having to
        catch all keypresses """
    _submit_handler = None

    def _set_submit(self, val):
        self._submit_handler = val
        self.tk.queue(Task("Handler installed on %s %d" % (self.name, self.id),
          {'control':self.name, "id":self.id, "action":"handler", "type":"submit"}))

    def _get_submit(self):
        return self._submit_handler

    submit = property(_get_submit, _set_submit)    

