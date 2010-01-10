from rctk.task import Task

class Event(object):
    def __init__(self, control):
        self.control = control

class ClickEvent(Event):
    pass

class ChangeEvent(Event):
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
