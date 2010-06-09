from copy import copy

from rctk.widgets import Panel, StaticText
from rctk.layouts import VBox


class Collection(Panel):
    name = "collection"
    
    def __init__(self, tk, widget_class, items=[], **properties):
        super(Collection, self).__init__(tk, **properties)
        self.setLayout(VBox())
        self.widget_class = widget_class
        self._items = []
        self.extend(items)
    
    def append(self, x):
        w = self.widget_class(self.tk, x)
        self._items.append((x, w))
        super(Collection, self).append(w)
        self.layout()

    def remove(self, x):
        for (a, w) in copy(self._items):
            if x == a:
                super(Collection, self).remove(w)
                self._items.remove((x, w))
        self.layout()
    
    def extend(self, L):
        for x in L:
            self.append(x)
    
    def clear(self):
        for w in copy(self._controls):
            super(Collection, self).remove(w)
        self._items = []
        self.layout()
    
    
