from rctk.tests.base import BaseTest
from rctk.widgets.control import Control, Attribute

class TestSyncedControl(BaseTest):
    def test_single_attribute(self):
        class TestControl(Control):
            a = Attribute("default")

        t = TestControl(self.tk)
        assert len(self.tk._queue) == 1
        assert self.tk._queue[0]._task['action'] == 'create'
        assert self.tk._queue[0]._task['a'] == 'default'

    def test_single_attribute_nondefault(self):
        class TestControl(Control):
            a = Attribute("default")

        t = TestControl(self.tk, a="nondefault")
        assert len(self.tk._queue) == 1
        assert self.tk._queue[0]._task['action'] == 'create'
        assert self.tk._queue[0]._task['a'] == 'nondefault'

    def test_update(self):
        class TestControl(Control):
            a = Attribute("default")

        t = TestControl(self.tk, a="nondefault")
        self.tk._queue.pop() # pop the create task
        t.a = 'updated'
        assert len(self.tk._queue) == 1
        assert self.tk._queue[0]._task['action'] == 'update'
        assert self.tk._queue[0]._task['update']['a'] == 'updated'

    def test_create_filter_default(self):
        def filter(a):
            return a[::-1]

        class TestControl(Control):
            a = Attribute("default", filter=filter)

        t = TestControl(self.tk)
        assert self.tk._queue[0]._task['a'] == 'tluafed'

    def test_create_filter_nondefault(self):
        def filter(a):
            return a[::-1]

        class TestControl(Control):
            a = Attribute("default", filter=filter)

        t = TestControl(self.tk, a="nondefault")
        assert self.tk._queue[0]._task['a'] == 'tluafednon'

    def test_update_filter(self):
        def filter(a):
            return a[::-1]

        class TestControl(Control):
            a = Attribute("default", filter=filter)

        t = TestControl(self.tk)
        self.tk._queue.pop() # pop the create task
        t.a = 'updated'
        assert len(self.tk._queue) == 1
        assert self.tk._queue[0]._task['action'] == 'update'
        assert self.tk._queue[0]._task['update']['a'] == 'detadpu'

    def test_remote_sync(self):
        class TestControl(Control):
            a = Attribute("default")
        t = TestControl(self.tk)
        t.sync(a="synced")
        assert t.a == "synced"

    def test_scenario(self):
        """ a more complete, slightly more complex scenario """
        def filter(a):
            return a[::-1]

        class TestControl(Control):
            a = Attribute("default", filter=filter)
            b = Attribute(1, Attribute.NUMBER)

        t = TestControl(self.tk, b=2)
        assert len(self.tk._queue) == 1
        assert self.tk._queue[0]._task['action'] == 'create'
        assert self.tk._queue[0]._task['a'] == 'tluafed'
        assert self.tk._queue[0]._task['b'] == 2
        self.tk._queue.pop()

        t.a = "updated"
        t.b = 3
        assert len(self.tk._queue) == 2
        assert self.tk._queue[0]._task['update']['a'] == 'detadpu'
        assert self.tk._queue[1]._task['update']['b'] == 3

        t.sync(a="synced", b=100)
        assert t.a == "synced"
        assert t.b == 100

## TODO: Integratie attributes into xmlbuilder, test it.


# test (remote) sync of attribute
