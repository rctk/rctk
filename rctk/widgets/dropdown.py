from rctk.widgets.control import Control, Attribute

from rctk.task import Task
from rctk.event import Clickable

class Dropdown(Control, Clickable):
    """
        Display a dropdown containing values. The caller must supply
        items as tuples (key, label), label will be used for presentation,
        key can be used to identify the selection made. Keys can be any
        type of object.

        The dropdown widget will uniquely enumerate the options itself, it
        will not use the provided keys. These enumerated indexes will be used
        as "selection" and will have no direct meaning outside the Dropdown

        A Dropdown is clickable, the handler will receive the item selected
        in the eventobject as "key".

        The default setup is no selection at all.

        TODO:
        - support index for insertion
        - support removal of items
        - make the entire user-defined keystuff optional, provide a way to map
          the selection to the label (or just use label as key?)
    """
    name = "dropdown"

    # selection synchronizes the selected state with the client. It's
    # not to be accessed directly since it doesn't directly contain the
    # items configured on the Dropdown
    selection = Attribute(None, Attribute.NUMBER)


    def __init__(self, tk, items=(), **properties):
        self.indexer = 0

        self.items = []
        for (k, v) in items:
            self.items.append((self.indexer, (k, v)))
            self.indexer += 1

        super(Dropdown, self).__init__(tk, **properties)

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
    ## The value property will map the user-defined keys
    ## to the internal indexes
    def _get_value(self):
        for (idx, (key, value)) in self.items:
            if idx == self.selection:
                return key
        return None

    def _set_value(self, v):
        for (idx, (key, value)) in self.items:
            if v == key:
                self.selection = idx
                return
        raise KeyError(v)

    value = property(_get_value, _set_value)

    def reset(self):
        """ set the selection to the first value """
        if self.items:
            self.selection = [self.items[0][0]]

    def clear(self):
        self._items = []
        self.selection = None # XXX this will create a redundant task
        ## no strict need to reset indexer
        self.tk.queue(Task("Dropdown cleared id %d" % self.id,
         {'control':self.name, "id":self.id, "action":"update", 
          "update":{"clear":True}}))

    def __repr__(self):
        return '<%s name="%s" id=%d items %s>' % (self.__class__.__name__, self.name, self.id, repr(self.items))
