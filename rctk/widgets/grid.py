from control import Control

from rctk.task import Task

class Column(object):
    """ configures a single column """
    # http://www.trirand.com/jqgridwiki/doku.php?id=wiki:colmodel_options
    id = 0

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

    # (sort) types. Create DateColumn/IntColumn etc in stead, and move
    # datfmt to DateColumn?
    TEXT = "text"
    INT = "int"
    FLOAT = "float"
    DATE = "date"

    def __init__(self, name, resizable=True, sortable=True, 
                 width=None, align=None, sorttype=TEXT, datefmt=None):
        self.name = name
        self.id = "col_%d" % Column.id
        Column.id += 1
        self.resizable = resizable
        self.sortable = sortable
        self.width = width
        self.align = align
        self.sorttype = sorttype
        self.datefmt = datefmt

    @property
    def model(self):
        m = dict(name=self.id, resizable=self.resizable, sortable=self.sortable)
        if self.width is not None:
            m['width'] = self.width
        if self.align is not None:
            m['align'] = self.align
        if self.datefmt is not None:
            m['datefmt'] = self.datefmt

        m['index'] = self.id # what else?
        m['sorttype'] = self.sorttype

        return m
        
class Row(object):
    def __init__(self, id, data):
        self.id = id
        self.data = data

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

    FIRST = "first"
    LAST = "last"
    BEFORE = "before"
    AFTER = "after"

    def __init__(self, tk, cols):
        self.cols = cols
        self.rowcounter = 1
        super(Grid, self).__init__(tk)
        self.rows = []
        self.rowmap = {}

    def create(self):
        self.tk.create_control(self, 
            colNames=[c.name for c in self.cols],
            colModel=[c.model for c in self.cols])

    def add(self, data, rowid=-1, position=LAST, srcrowid=-1):
        """ 
            Add a row of data. You can pass a rowid to identify
            the row, or else one will be generated (and returned).

            position can be FIRST, LAST, BEFORE or AFTER,
            the default is LAST.

            BEFORE and AFTER are relative to srcrowid. Not specifying
            a srcrowid will have unpredictable results if BEFORE
            or AFTER is used
        """
        if rowid == -1:
            rowid = self.rowcounter
            self.rowcounter += 1

        rowid = str(rowid)

        if position in (Grid.BEFORE, Grid.AFTER) and srcrowid == -1:
            raise ValueError, "Grid.BEFORE or Grid.AFTER used but no srcrowid specified"

        row = Row(rowid, data)
        self.rows.append(row)
        self.rowmap[rowid] = row

        datadict = dict(zip((c.id for c in self.cols), data))

        self.tk.queue(Task("Grid update (add row) id %d rowid %s" % 
                       (self.id, rowid),
                       {'control':self.name, 
                        'id':self.id, 
                        'action':'update',
                        'update':{'addrow':
                           {'id':rowid, 
                            'data':datadict, 
                            'position':position,  
                            'srcrowid':srcrowid
                           }
                          }
                        }))
        return rowid

    def clear(self):
        """ clear the entire grid """
        ## leave rowcounter untouched, regard those id's as invalid
        self.rows = []
        self.rowmap = {}
        self.tk.queue(Task("Grid cleared id %d" % self.id,
          {'control':self.name,
           'id':self.id,
           'action':'update',
           'update':{'clear':True}}))
