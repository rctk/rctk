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
    def test_1(self):
        layout = NewLayout(rows=3, columns=3)
        layout.allocate(0,0)
        res = layout.find(rowspan=2, colspan=3)
        assert res == (0, 1)

    def test_2(self):
        layout = NewLayout(rows=3, columns=3)
        layout.allocate(1,1)
        res = layout.find(rowspan=2, colspan=3)
        assert res is None
