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


class TestNewLayout(object):
    def test_fixed_trivial(self):
        layout = NewLayout(rows=1, columns=1)
        assert layout.available_positions() is not None
        layout.allocate(0, 0)
        assert layout.available_positions() is None
