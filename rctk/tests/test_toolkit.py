from rctk.tests.base import BaseTest

class TestToolkit(BaseTest):
    def test_root(self):
        """ assert there's a root and it has an id of 0 """
        assert self.tk.root().id == 0

    def test_queue(self):
        """ initially, the queue should be empty """
        assert len(self.tk._queue) == 0

    def test_controls(self):
        """ initially, there should be one control, the root """
        from rctk.widgets.root import Root

        assert len(self.tk._controls) == 1
        assert self.tk._controls.keys() == [0]
        assert type(self.tk._controls[0]) == Root

