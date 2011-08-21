from rctk.tests.base import BaseTest, build_task_queue

from rctk.widgets import Dropdown

class TestDropdown(BaseTest):
    def test_empty(self):
        w = Dropdown(self.tk)
        assert w.selection is None

    def test_empty_then_add(self):
        w = Dropdown(self.tk)
        w.add('1', 'a')
        assert w.selection is None
        assert w.value is None

    def test_nonempty(self):
        w = Dropdown(self.tk, (('1', 'a'), ('2', 'b')))
        assert w.selection is None
        assert w.value is None

    def test_selectionmade(self):
        w = Dropdown(self.tk, (('1', 'a'), ('2', 'b')))
        self.tk.handle("task", queue=build_task_queue("sync", type="sync", id=w.id, selection=1))
        assert w.selection == 1
        assert w.value == '2'

    def test_setselection(self):
        w = Dropdown(self.tk, (('1', 'a'), ('2', 'b')))
        self.tk.clear() # clear queue
        w.value = '2'
        assert len(self.tk._queue) == 1
        assert self.tk._queue[0]._task['action'] == 'update'
        assert self.tk._queue[0]._task['id'] == w.id
        assert self.tk._queue[0]._task['update'] == {'selection':1}

