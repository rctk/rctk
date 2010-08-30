from rctk.layouts.layouts import Layout, LayoutException

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

    EMPTY = None
    FULL = object()

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

        self.grid = []
        self.calculated_rows = rows
        self.calculated_cols = columns

    def allocate(self, row, column, rowspan=1, colspan=1):
        """ allocate a cell. Shouldn't be allocated already """
        if self.rows is not None and self.columns is not None:
            cell = row * self.columns + column
            if self.grid[cell] is self.FULL:
                ## spans!
                raise LayoutException("Cell row=%d column=%d already allocated" % (row, column))

            self.grid[cell] = self.FULL

        if self.columns is None:
            cell = column * self.rows + row
            if self.grid[cell] is self.FULL:
                ## spans!
                raise LayoutException("Cell row=%d column=%d already allocated" % (row, column))

            self.grid[cell] = self.FULL
            ## spans!

        
    def available_positions(self):
        ## fixed grid
        if self.rows is not None and self.columns is not None:
            for r in range(0, self.rows):
                for c in range(0, self.columns):
                    idx = r * self.columns + c
                    if idx >= len(self.grid):
                        # unexplored pad. Expand grid, we've found something
                        self.grid.append(None)
                        return r, c
                    elif self.grid[idx] is self.EMPTY:
                        return r, c

            return None # full

        ## columns are bound, grow vertically
        if self.rows is not None:
            r = 0
            while True:
                for c in range(0, self.columns):
                    idx = r * self.columns + c
                    if idx >= len(self.grid):
                        # unexplored pad. Expand grid, we've found something
                        self.grid.append(None)
                        return r, c
                    elif self.grid[idx] is self.EMPTY:
                        return r, c
                r += 1
            return None # full

        ## rows are bound, grow horizontally
        c = 0
        while True:
            for r in range(0, self.rows):
                idx = c * self.rows + r
                # ...
                
    def space_available(self, row, column, rowspan=1, colspan=1):
        # verify a space is available, possibly expanding the grid

        if self.columns is not None and colspan > self.columns:
            raise LayoutException("Colspan of %d too wide for grid with %d columns" % (colspan, self.columns))

        if self.rows is not None and rowspan > self.rows:
            raise LayoutException("Rowspan of %d too high for grid with %d rows" % (rowspan, self.rows))

        for position in self.available_positions():
            pass #...

    def find(self, row=None, column=None, rowspan=1, colspan=1):

        if row is None and col is None:
            find-first-free
        elif row is None:
            find-first-free(column)
        elif col is None:
            find-first-free(row)
        else:
            check (row, column) is available

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

        
