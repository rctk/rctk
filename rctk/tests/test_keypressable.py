from rctk.tests.base import BaseTest, build_task_queue

class KeypressCounter(object):
    def __init__(self):
        self.count = 0
        self.lastcontrol = None

    def __call__(self, event):
        self.lastcontrol = event.control
        self.count += 1

from rctk.event import Keypressable

class BaseKeypressableTest(BaseTest):
    widget = None

    ## overlap with test_controls
    def create_widget(self):
        return self.widget(self.tk)

    def test_class(self):
        w = self.create_widget()
        assert isinstance(w, Keypressable)

    def test_keypress_task(self):
        c = KeypressCounter()
        w = self.create_widget()
        self.tk.clear() ## clear create event
        w.keypress = lambda event: None
        assert len(self.tk._queue) == 1
        assert self.tk._queue[0]._task['action'] == 'handler'
        assert self.tk._queue[0]._task['type'] == 'keypress'
        assert self.tk._queue[0]._task['control'] == self.widget.name
        assert self.tk._queue[0]._task['id'] == w.id

    def test_keypress(self):
        c = KeypressCounter()
        w = self.create_widget()
        w.keypress = c
        assert c.count == 0

        ## simulate a remote click event
        self.tk.handle("task", queue=build_task_queue("event", type="keypress", id=w.id))

        assert c.count == 1
        assert c.lastcontrol == w

    def test_disabled(self):
        """ assert that disabled controls don't handle presses """
        c = KeypressCounter()
        w = self.create_widget()
        w.keypress = c
        w.enabled = False
        assert c.count == 0

        ## simulate a remote keypress event
        self.tk.handle("task", queue=build_task_queue("event", type="keypress", id=w.id))
        assert c.count == 0


from rctk.widgets.text import Text
class TestKeypressableText(BaseKeypressableTest):
    widget = Text
    def create_widget(self):
        return self.widget(self.tk)

