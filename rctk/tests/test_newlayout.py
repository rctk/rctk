import py.test

from rctk.layouts.newlayout import Grid, NewLayout, LayoutException

class TestGrid(object):
    def test_iterator_fixed(self):
        g = Grid(rows=2, columns=3)
        walk = list(iter(g))
        assert walk == [(0, 0), (0, 1), (0, 2),
                        (1, 0), (1, 1), (1, 2)]

    def test_iterator_columnfixed(self):
        g = Grid(columns=2)
        i = iter(g)
        assert next(i) == (0, 0)
        assert next(i) == (0, 1)
        assert next(i) == (1, 0)
        assert next(i) == (1, 1)
        assert next(i) == (2, 0)

    def test_iterator_rowfixed(self):
        g = Grid(rows=2)
        i = iter(g)
        assert next(i) == (0, 0)
        assert next(i) == (1, 0)
        assert next(i) == (0, 1)
        assert next(i) == (1, 1)
        assert next(i) == (0, 2)

    def test_expand_fixed(self):
        """ a fresh grid should size itself appropriately """
        g = Grid(rows=2, columns=2)
        assert g.get(0, 0) is Grid.EMPTY
        assert g.get(1, 0) is Grid.EMPTY
        assert g.get(0, 1) is Grid.EMPTY
        assert g.get(1, 1) is Grid.EMPTY

    def test_expand_columnfixed(self):
        """ grow vertically infinitely """
        g = Grid(columns=2)
        assert g.get(0, 0) is Grid.EMPTY
        assert g.get(0, 1) is Grid.EMPTY
        assert g.get(5, 1) is Grid.EMPTY
        assert g.get(3, 0) is Grid.EMPTY

    def test_expand_rowfixed(self):
        """ grow horizontally infinitely """
        g = Grid(rows=2)
        assert g.get(0, 0) is Grid.EMPTY
        assert g.get(0, 1) is Grid.EMPTY
        assert g.get(0, 6) is Grid.EMPTY
        assert g.get(1, 0) is Grid.EMPTY
        assert g.get(1, 12) is Grid.EMPTY

class TestGridSize(object):
    def test_fixed(self):
        g = Grid(rows=3, columns=6)
        assert g.size() == (3, 6)

    def test_rows_empty(self):
        g = Grid(rows=3)
        g.size() == (3, 1)

    def test_columns_empty(self):
        g = Grid(columns=3)
        g.size() == (1, 3)

    def test_rows_minimal(self):
        g = Grid(rows=3)
        g.set(0, 0, Grid.FULL)
        g.size() == (3, 1)

    def test_columns_minimal(self):
        g = Grid(columns=3)
        g.set(0, 0, Grid.FULL)
        g.size() == (1, 3)

    def test_rows_fit(self):
        g = Grid(rows=2)
        g.set(0, 0, Grid.FULL)
        g.set(0, 1, Grid.FULL)
        g.set(1, 0, Grid.FULL)
        g.set(1, 1, Grid.FULL)
        g.size() == (2, 2)

    def test_columns_fit(self):
        g = Grid(columns=2)
        g.set(0, 0, Grid.FULL)
        g.set(0, 1, Grid.FULL)
        g.set(1, 0, Grid.FULL)
        g.set(1, 1, Grid.FULL)
        g.size() == (2, 2)

    def test_rows_extra(self):
        g = Grid(rows=2)
        g.set(0, 0, Grid.FULL)
        g.set(0, 1, Grid.FULL)
        g.set(1, 0, Grid.FULL)
        g.set(1, 1, Grid.FULL)
        g.set(0, 2, Grid.FULL)
        g.size() == (2, 3)

    def test_columns_extra(self):
        g = Grid(columns=2)
        g.set(0, 0, Grid.FULL)
        g.set(0, 1, Grid.FULL)
        g.set(1, 0, Grid.FULL)
        g.set(1, 1, Grid.FULL)
        g.set(2, 0, Grid.FULL)
        g.size() == (3, 2)

class TestNewLayoutTrivial(object):
    """ trivial cases, single  cells, no colspans """
    def test_available_fixed(self):
        layout = NewLayout(rows=1, columns=1)
        assert layout.available_positions() is not None
        layout.allocate(0, 0)
        assert layout.available_positions() is None

    def test_available_rowfixed(self):
        layout = NewLayout(rows=1)
        assert layout.available_positions() is not None
        layout.allocate(0, 0)
        assert layout.available_positions() is not None
        assert layout.available_positions() == (0, 1)

    def test_available_colfixed(self):
        layout = NewLayout(columns=1)
        assert layout.available_positions() is not None
        layout.allocate(0, 0)
        assert layout.available_positions() is not None
        assert layout.available_positions() == (1, 0)

    def test_allocate_fixed(self):
        layout = NewLayout(rows=1, columns=1)
        layout.allocate(0, 0)
        py.test.raises(LayoutException, layout.allocate, 0, 0)

    def test_allocate_rowfixed(self):
        layout = NewLayout(rows=1)
        layout.allocate(0, 0)
        py.test.raises(LayoutException, layout.allocate, 0, 0)

    def test_allocate_colfixed(self):
        layout = NewLayout(columns=1)
        layout.allocate(0, 0)
        py.test.raises(LayoutException, layout.allocate, 0, 0)

    def test_available_toobig_fixed(self):
        layout = NewLayout(rows=2, columns=2)

        def fail1():
            layout.space_available(0, 0, rowspan=3, colspan=2)
        py.test.raises(LayoutException, fail1)
        def fail2():
            layout.space_available(0, 0, rowspan=2, colspan=3)
        py.test.raises(LayoutException, fail2)

    def test_available_toobig_rowfixed(self):
        layout = NewLayout(rows=2)
        def fail():
            layout.space_available(0, 0, rowspan=3, colspan=10)
        py.test.raises(LayoutException, fail)

    def test_available_toobig_rowfixed(self):
        layout = NewLayout(columns=2)
        def fail():
            layout.space_available(0, 0, rowspan=20, colspan=3)
        py.test.raises(LayoutException, fail)

class TestNewLayoutSpans(object):
    def test_fit(self):
        layout = NewLayout(rows=2, columns=2)
        res = layout.find(rowspan=2, colspan=2)
        assert res == (0, 0)

    def test_available(self):
        layout = NewLayout(rows=3, columns=3)
        layout.allocate(0,0)
        res = layout.find(rowspan=2, colspan=3)
        assert res == (1, 0)

    def test_notavailable(self):
        layout = NewLayout(rows=3, columns=3)
        layout.allocate(1,1)
        res = layout.find(rowspan=2, colspan=3)
        assert res is None

    def test_blocks(self):
        layout = NewLayout(rows=4, columns=4)
        layout.allocate(0, 0, colspan=2, rowspan=2)
        res = layout.find(rowspan=2, colspan=2)
        assert res == (0, 2)
        layout.allocate(0, 2, colspan=2, rowspan=2)
        res = layout.find(rowspan=2, colspan=2)
        assert res == (2, 0)
        layout.allocate(2, 0, colspan=2, rowspan=2)
        res = layout.find(rowspan=2, colspan=2)
        assert res == (2, 2)
        layout.allocate(2, 2, colspan=2, rowspan=2)
        res = layout.find(rowspan=2, colspan=2)
        assert res == None

    def test_allocate_refused_row(self):
        layout = NewLayout(rows=4, columns=4)
        layout.allocate(0, 1)
        # so far so good. Try to allocate something with a colspan of 2
        # at 0,0
        py.test.raises(LayoutException, layout.allocate, 0, 0, 1, 2)

    def test_allocate_refused_col(self):
        layout = NewLayout(rows=4, columns=4)
        layout.allocate(1, 0)
        # so far so good. Try to allocate something with a colspan of 2
        # at 0,0
        py.test.raises(LayoutException, layout.allocate, 0, 0, 2, 1)

class TestSingleRow(object):
    def test_grow(self):
        layout = NewLayout(rows=1)
        layout.allocate(0, 0)
        assert layout.find() == (0, 1)
        layout.allocate(0, 1)
        assert layout.find() == (0, 2)

    def test_gap(self):
        layout = NewLayout(rows=1)
        layout.allocate(0, 1)
        assert layout.find() == (0, 0)

    def test_largegap(self):
        layout = NewLayout(rows=1)
        layout.allocate(0, 10)
        assert layout.find() == (0, 0)

    def test_no_secondrow(self):
        layout = NewLayout(rows=1)
        py.test.raises(LayoutException, layout.allocate, 1, 0)

class TestDoubleRow(object):
    def test_grow(self):
        layout = NewLayout(rows=2)
        layout.allocate(0, 0)
        assert layout.find() == (1, 0)
        layout.allocate(1, 0)
        assert layout.find() == (0, 1)

    def test_gap(self):
        layout = NewLayout(rows=2)
        layout.allocate(1, 0)
        assert layout.find() == (0, 0)
    
    def test_largegap(self):
        layout = NewLayout(rows=2)
        layout.allocate(1, 5)
        assert layout.find() == (0, 0)

class TestSingleColumn(object):
    def test_grow(self):
        layout = NewLayout(columns=1)
        layout.allocate(0, 0)
        assert layout.find() == (1, 0)
        layout.allocate(1, 0)
        assert layout.find() == (2, 0)

    def test_gap(self):
        layout = NewLayout(columns=1)
        layout.allocate(1, 0)
        assert layout.find() == (0, 0)

    def test_largegap(self):
        layout = NewLayout(columns=1)
        layout.allocate(10, 0)
        assert layout.find() == (0, 0)

    def test_no_secondcolumn(self):
        layout = NewLayout(columns=1)
        py.test.raises(LayoutException, layout.allocate, 0, 1)

class TestDoubleColumn(object):
    def test_grow(self):
        layout = NewLayout(columns=2)
        layout.allocate(0, 0)
        assert layout.find() == (0, 1)
        layout.allocate(0, 1)
        assert layout.find() == (1, 0)

    def test_gap(self):
        layout = NewLayout(columns=2)
        layout.allocate(0, 1)
        assert layout.find() == (0, 0)
    
    def test_largegap(self):
        layout = NewLayout(columns=2)
        layout.allocate(5, 1)
        assert layout.find() == (0, 0)

dummy = object()

class TestFixedComplex1(object):
    """ a random, fixed layout """
    def setup_method(self, method):
        self.layout = NewLayout(rows=5, columns=7)

    def test_blocks(self):
        self.layout.append(dummy, rowspan=3, colspan=3)
        self.layout.append(dummy, rowspan=2, colspan=2)
        self.layout.append(dummy, rowspan=2, colspan=2)
        self.layout.append(dummy, rowspan=3, colspan=2)
        self.layout.append(dummy, rowspan=3, colspan=2)
        self.layout.append(dummy, rowspan=2, colspan=3)
        assert self.layout.find() is None

    def test_cells(self):
        for i in range(0, 5*7):
            self.layout.append(dummy)
        assert self.layout.find() is None

    def test_widecells(self):
        for i in range(0, 5):
            self.layout.append(dummy, colspan=7)
        assert self.layout.find() is None

class TestComplex1(object):
    """ Same as TestComplex but only columns fixed, rows grow """
    def setup_method(self, method):
        self.layout = NewLayout(columns=7)

    def test_blocks(self):
        self.layout.append(dummy, rowspan=3, colspan=3)
        self.layout.append(dummy, rowspan=2, colspan=2)
        self.layout.append(dummy, rowspan=2, colspan=2)
        self.layout.append(dummy, rowspan=3, colspan=2)
        self.layout.append(dummy, rowspan=3, colspan=2)
        self.layout.append(dummy, rowspan=2, colspan=3)
        assert self.layout.find() == (5, 0)

    def test_cells(self):
        for i in range(0, 5*7):
            self.layout.append(dummy)
        assert self.layout.find() == (5, 0)

    def test_widecells(self):
        for i in range(0, 5):
            self.layout.append(dummy, colspan=7)
        assert self.layout.find() == (5, 0)
