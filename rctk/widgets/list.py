from rctk.widgets.control import Attribute, Control
from rctk.task import Task
from rctk.event import Clickable, DoubleClickable

class List(Control, Clickable, DoubleClickable): # confusing name - list vs List?
    name = "list"
    """
        A list is functionally the same as a Dropdown, it's just rendered
        differently and it can display a number of items at once.
    """
    multiple = Attribute(False, Attribute.BOOLEAN)
    selection = Attribute([], Attribute.NUMBER) # List of Number actually
    size = Attribute(0, Attribute.NUMBER)
    selection = Attribute([], Attribute.NUMBER)


    def __init__(self, tk, items=(), **properties):
        self.indexer = 0

        self.items = []
        for (k, v) in items:
            self.items.append((self.indexer, (k, v)))
            self.indexer += 1

        super(List, self).__init__(tk, **properties)

    def create(self):
        self.tk.create_control(self, items=self._items())

    def add(self, key, value):
        """ this adds a new entry to the bottom. Removing items or selecting
            an insertion position is not yet possible """
        ## the first entry is the initial default. Check if this is the first entry
        self.items.append((self.indexer, (key, value)))

        self.tk.queue(Task("Dropdown update id %d items '%s'" %
          (self.id, repr(self.items)),
         {'control':self.name, "id":self.id, "action":"update",
          "update":{"item":(self.indexer, value)}}))
        self.indexer += 1

    def _items(self):
        return [(idx, label) for (idx, (k, label)) in self.items]

    ##
    ## The value property will map the user defined key(s)
    ## to the internal indexes. No matter what the mode of this
    ## List is (multiple or single), sequences of values
    ## must be assigned and will be returned.
    def _get_value(self):
        r = []
        for (idx, (key, value)) in self.items:
            if idx in self.selection:
                r.append(key)
        return r

    def _set_value(self, v):
        if not self.multiple and len(v) > 1:
            raise ValueError("Can assign at most one value to single List")
        s = []
        for (idx, (key, value)) in self.items:
            if key in v:
                s.append(idx)
        self.selection = s
        return

    value = property(_get_value, _set_value)

    def reset(self):
        """ set the selection to the first value """
        if self.items:
            self.selection = [self.items[0][0]]

    def clear(self):
        self._items = []
        self.selection = [] # XXX this will create a redundant task
        ## no strict need to reset indexer
        self.tk.queue(Task("Dropdown cleared id %d" % self.id,
         {'control':self.name, "id":self.id, "action":"update", 
          "update":{"clear":True}}))

    def __repr__(self):
        return '<%s name="%s" id=%d multiple=%s items %s>' % (self.__class__.__name__, self.name, self.id, self.multiple, repr(self.items))
