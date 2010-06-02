from rctk.tests.base import BaseTest


class BaseContainerTest(BaseTest):
    """
        Test basic container type behaviour
    """
    container = None
    
    def create_widgets(self):
        c = self.container(self.tk)
        w = self.container(self.tk)
        self.tk.clear()
        return (c, w)
    
    def test_append(self):
        c, w = self.create_widgets()
        c.append(w)
        task = self.tk._queue.pop()
        assert task._task['action'] == 'append'
        assert task._task['id'] == c.id
        assert task._task['child'] == w.id
        assert w in c._controls
    
    def test_remove(self):
        c, w = self.create_widgets()
        c.append(w)
        self.tk.clear() # ignore append task
        c.remove(w)
        task = self.tk._queue.pop()
        assert task._task['action'] == 'remove'
        assert task._task['id'] == c.id
        assert task._task['child'] == w.id
        assert w not in c._controls
    
    def test_do_not_append_self(self):
        c, w = self.create_widgets()
        c.append(c)
        assert len(self.tk._queue) == 0
        assert c not in c._controls
    
    def test_do_not_remove_if_not_appended(self):
        c, w = self.create_widgets()
        assert w not in c._controls
        c.remove(w)
        assert len(self.tk._queue) == 0
        assert w not in c._controls
    


from rctk.widgets.panel import Panel
class TestPanelWidget(BaseContainerTest):
    container = Panel

