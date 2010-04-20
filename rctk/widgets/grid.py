from control import Control

class Column(object):
    """ configures a single column """
    # http://www.trirand.com/jqgridwiki/doku.php?id=wiki:colmodel_options
    id = 0

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

    def __init__(self, name, resizable=True, sortable=True, 
                 width=None, align=None):
        self.name = name
        self.id = "col_%d" % Column.id
        Column.id += 1
        self.resizable = resizable
        self.sortable = sortable
        self.width = width
        self.align = align

    @property
    def model(self):
        m = dict(name=self.id, resizable=self.resizable, sortable=self.sortable)
        if self.width is not None:
            m['width'] = self.width
        if self.align is not None:
            m['align'] = self.align
        m['index'] = self.id # what else?
        return m
        
class Grid(Control):
    """
        A table-like list structure:

        - typed columns
        - context menu
        - sorting
        - adding new columns
        - handle events
        - possibly inline data entry
    """
    name = "grid"

    def __init__(self, tk, cols):
       self.cols = cols
       super(Grid, self).__init__(tk)

    def create(self):
        self.tk.create_control(self, 
            colNames=[c.name for c in self.cols],
            colModel=[c.model for c in self.cols])

    def add(self, row):
       """ add a row of data """
       pass
