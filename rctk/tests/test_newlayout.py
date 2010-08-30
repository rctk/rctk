from rctk.layouts.newlayout import NewLayout, LayoutException

class TestNewLayout(object):
    def test_fixed_trivial(self):
        layout = NewLayout(rows=1, columns=1)
        assert layout.available_positions() is not None
        layout.allocate(0, 0)
        assert layout.available_positions() is None
