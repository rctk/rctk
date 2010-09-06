from rctk.task import Task

class Event(object):
    def __init__(self, control, **kw):
        self.control = control
        self.args = kw

    @classmethod
    def invoke(cls, id, control, **kw):
        """ default is to map to a method equal to the eventid """
        handler = getattr(control, id, None)
        if handler:
            handler(cls(control, **kw))

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


class Dispatcher(object):
    events = {}

    def register(self, id, eventclass):
        self.events[id] = eventclass

    def __call__(self, id, control, **kw):
        """ 
            invoke an event. This may raise a keyerror for unregistered events 
        """
        self.events[id].invoke(id, control, **kw)

dispatcher = Dispatcher()

dispatcher.register('click', ClickEvent)
dispatcher.register('change', ChangeEvent)
dispatcher.register('submit', SubmitEvent)
