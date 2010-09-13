from rctk.layouts.layouts import Layout, LayoutException
import math

class Cell(object):
    def __init__(self, o, row, column, rowspan=1, colspan=1, **options):
        self.o = o
        self.row = row
        self.column = column
        self.rowspan = rowspan
        self.colspan = colspan
        self.options = options

    def data(self):
        base = self.options.copy()
        base['controlid'] = self.o.id
        base['row'] = self.row
        base['column'] = self.column
        base['rowspan'] = self.rowspan
        base['colspan'] = self.colspan
        return base

class Grid(object):
    """ basic dynamic grid abstraction """
    EMPTY = None
    FULL = object()

    def __init__(self, rows=None, columns=None):
        self.rows = rows
        self.columns = columns
        self._grid = []

    def __iter__(self):
        ## left to right, top to bottom, fixed size
        if self.rows is not None and self.columns is not None:
            for r in range(0, self.rows):
                for c in range(0, self.columns):
                    yield (r, c)
            raise StopIteration()

        ## left to right, top to bottom, grow vertically (forever!)
        if self.rows is None:
            r = 0
            while True:
                for c in range(0, self.columns):
                    yield (r, c)
                r += 1

        ## top to bottom, left to right, grow horizontally
        c = 0
        while True:
            for r in range(0, self.rows):
                yield (r, c)
            c += 1

    def _get_index(self, row, column):
        if self.columns is not None:
            idx = row * self.columns + column
        else:
            idx = column * self.rows + row
        return idx

    def _expand(self, idx):
        """ expand the grid so <idx> becomes a valid index """
        while len(self._grid) <= idx:
            self._grid.append(None)

    def get(self, row, column):
        idx = self._get_index(row, column)
        self._expand(idx)
        return self._grid[idx]

    def set(self, row, column, val):
        idx = self._get_index(row, column)
        self._expand(idx)
        self._grid[idx] = val

    def size(self):
        count = len(self._grid)

        if self.columns is not None and self.rows is not None:
            rows = self.rows
            columns = self.columns
        elif self.columns is not None:
            columns = self.columns
            rows = int(math.ceil(count / float(self.columns))) or 1
        else:
            columns = int(math.ceil(count / float(self.rows))) or 1
            rows = self.rows
        return (rows, columns) 


class NewLayout(Layout):
    """
        This layout uses a "Grid" to keep track of which
        cells have been allocated, but the actual end result
        of the layout is a list of cells with position, spanning 
        and options, and a reference to the object that's placed
        in this cell
    """
    type = "new"
    
    CENTER = 0
    N = NORTH = 1
    E = EAST = 2
    S = SOUTH = 4
    W = WEST = 8

    def __init__(self, rows=None, columns=None, static=False,
                 padx=0, pady=0, ipadx=0, ipady=0, sticky=CENTER):
        if rows is None and columns is None:
            raise LayoutException("Either rows or columns must be defined")
        self.rows = rows
        self.columns = columns
        self.static = static
        self.padx = padx
        self.pady = pady
        self.ipadx = ipadx
        self.ipady = ipady
        self.sticky = sticky

        self.grid = Grid(rows=rows, columns=columns)
        self.cells = []

    def allocate(self, row, column, rowspan=1, colspan=1):
        """ allocate a cell. Shouldn't be allocated already """
        if not self.space_available(row, column, rowspan, colspan):
            raise LayoutException("No %dx%d block available at (%d, %d)" % (rowspan, colspan, row, column))

        ## we know for sure it's available, so no further checks necessary
        for r in range(row, row+rowspan):
            for c in range(column, column+colspan):
                self.grid.set(r, c, Grid.FULL)

    def available_positions(self):
        for cell in iter(self.grid):
            if self.grid.get(*cell) is Grid.EMPTY:
                return cell

    def space_available(self, row, column, rowspan=1, colspan=1):
        # verify a space is available, possibly expanding the grid

        if self.columns is not None and colspan > self.columns:
            raise LayoutException("Colspan of %d too wide for grid with %d columns" % (colspan, self.columns))

        if self.rows is not None and rowspan > self.rows:
            raise LayoutException("Rowspan of %d too high for grid with %d rows" % (rowspan, self.rows))

        ## take actual gridsize / limits into account!
        if self.columns is not None and column+colspan > self.columns:
            return False
        if self.rows is not None and row+rowspan > self.rows:
            return False

        for r in range(row, row+rowspan):
            for c in range(column, column+colspan):
                if self.grid.get(r, c) is not Grid.EMPTY:
                    return False
        return True

    def find(self, rowspan=1, colspan=1):
        """ find a large enough area """
        for cell in iter(self.grid):
            row, column = cell
            if self.space_available(row, column, rowspan, colspan):
                return cell

    def append(self, o, row=-1, column=-1, padx=None, pady=None, ipadx=None, 
               ipady=None, sticky=None, colspan=1, rowspan=1):
        if padx is None:
            padx = self.padx
        if pady is None:
            pady = self.pady
        if ipadx is None:
            ipadx = self.ipadx
        if ipady is None:
            ipady = self.ipady
        if sticky is None:
            sticky = self.sticky

        if row == -1 and column == -1:
            r, c = self.find(rowspan, colspan)
            self.allocate(r, c, rowspan, colspan)
            self.cells.append(Cell(o, r, c, rowspan, colspan, 
              padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=sticky))
            return self.cells[-1]
        elif row != -1 and column != -1:
            self.allocate(row, column, rowspan, colspan)
            self.cells.append(Cell(o, r, c, rowspan, colspan, 
              padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, sticky=sticky))
            return self.cells[-1]
        else:
            raise LayoutException("Either both row and column must be set, or both must be undefined")
        
    def config(self):
        return dict(type="new",
                    size=self.grid.size(),
                    cells=[c.data() for c in self.cells])

