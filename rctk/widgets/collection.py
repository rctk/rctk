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

    def _append(self, x):
        w = self.widget_class(self.tk, x)
        self._items.append((x, w))
        super(Collection, self).append(w)

    def append(self, x):
        self._append(x)
        self.layout()

    def _remove(self, x):
        for (a, w) in copy(self._items):
            if x == a:
                super(Collection, self).remove(w)
                self._items.remove((x, w))
                w.destroy()

    def remove(self, x):
        self._remove(x)
        self.layout()

    def extend(self, L):
        for x in L:
            self._append(x)
        self.layout()

    def clear(self):
        for (a, w) in copy(self._items):
            self._remove(a)
        self.layout()


