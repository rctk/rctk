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
        """ Empty panels seem to break the layout manager. Insert
         a dummy StaticText for now and hide if from self by
         clearing self._controls. This is a really ugly hack and
         what we should do is fix the layout manager.
         FIXME: fix layout manger to support empty panels
        """ 
        dummy = StaticText(tk, 'Dummy Control')
        dummy.visible = False
        super(Collection, self).append(dummy)
        self._controls = [] # hide dummy control
        self.extend(items)
    
    def append(self, x):
        print "calling append"
        w = self.widget_class(self.tk, x)
        self._items.append((x, w))
        super(Collection, self).append(w)

    def remove(self, x):
        for (a, w) in copy(self._items):
            if x == a:
                super(Collection, self).remove(w)
                self._items.remove((x, w))
    
    def extend(self, L):
        for x in L:
            self.append(x)
    
    def clear(self):
        for w in copy(self._controls):
            super(Collection, self).remove(w)
        self._items = []
    
