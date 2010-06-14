from rctk.tests.base import BaseTest
from rctk.task import Task
from rctk.widgets import StaticText, Control

class BaseContainerTest(BaseTest):
    """
        Test basic container type behaviour
    """
    container = None
    
    def create_widgets(self):
        c = self.container(self.tk)
        w = StaticText(self.tk, 'Hello World')
        self.tk.clear()
        return (c, w)
    
    def test_append(self):
        c, w = self.create_widgets()
        c.append(w)
        task = self.tk._queue.pop()
        assert task == Task('Append %d to %d' % (w.id, c.id),
            {'action': 'append', 'id': c.id, 'child': w.id})
        assert w in c._controls
    
    def test_remove(self):
        c, w = self.create_widgets()
        c.append(w)
        self.tk.clear() # ignore append task
        c.remove(w)
        task = self.tk._queue.pop()
        assert task == Task('Remove %d from %d' % (w.id, c.id),
            {'action': 'remove', 'id': c.id, 'child': w.id})
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
    
    def test_remove_before_reappending(self):
        c1, w = self.create_widgets()
        c2 = self.container(self.tk)
        self.tk.clear()
        c1.append(w)
        self.tk._queue.pop() # ignore first append task
        c2.append(w)
        remove_task = self.tk._queue.pop(0)
        append_task = self.tk._queue.pop()
        assert remove_task == Task('Remove %d from %d' % (w.id, c1.id),
            {'action': 'remove', 'id': c1.id, 'child': w.id})
        assert append_task == Task('Append %d to %d' % (w.id, c2.id),
            {'action': 'append', 'id': c2.id, 'child': w.id})

    def test_destroy_widget(self):
        c, w = self.create_widgets()
        c.append(w)
        self.tk.clear()
        w.destroy()
        self.tk._queue.pop(0) # ignore layout remove task
        assert w not in c._controls
        assert w not in c._controls_args
        assert w._parent == None
        assert w._append_args == None
    
    def test_destroy(self):
        c, w = self.create_widgets()
        c.append(w)
        self.tk.clear()
        c.destroy()
        assert len(c._controls) == 0
        assert len(c._controls_args) == 0
    

from rctk.widgets.panel import Panel
class TestPanelContainer(BaseContainerTest):
    container = Panel

from rctk.widgets.window import Window
class TestWindowContainer(BaseContainerTest):
    container = Window

from rctk.widgets.root import Root
class TestRootContainer(BaseContainerTest):
    container = Root

