from rctk.layouts.layouts import Layout, LayoutException

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

class NewLayout(Layout):
    type = "new"

    
    CENTER = 0
    N = NORTH = 1
    E = EAST = 2
    S = SOUTH = 4
    W = WEST = 8


    ## how to define flexible rows, columns?

    ## cols = None => grow horizontal
    ## rows = None => grow vertical
    ## rows, cols not None: raise if no fit

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

        self.calculated_rows = rows
        self.calculated_cols = columns

    def allocate(self, row, column, rowspan=1, colspan=1):
        """ allocate a cell. Shouldn't be allocated already """
        if self.grid.get(row, column) is not Grid.EMPTY:
            raise LayoutException("Cell row=%d column=%d already allocated" % (row, column))
        else:
            self.grid.set(row, column, Grid.FULL)

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

    def append(self, row, column, padx=None, pady=None, ipadx=None, 
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

        
