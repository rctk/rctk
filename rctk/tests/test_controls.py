from rctk.tests.base import BaseTest

from rctk.widgets import Control
from rctk.task import Task


#
# - test events, etc?
# - test clickable generically. Mixin with button, etc?

class BaseWidgetTest(BaseTest):
    """
        Test basic widget behaviour
    """
    widget = None

    def create_widget(self):
        return self.widget(self.tk)

    def test_create(self):
        w = self.create_widget()
        assert len(self.tk._queue) == 1
        assert self.tk._queue[0]._task['action'] == 'create'
        assert self.tk._queue[0]._task['control'] == self.widget.name
        assert self.tk._queue[0]._task['id'] == w.id
    
    def test_destroy(self):
        w = self.create_widget()
        self.tk.clear()
        w.destroy()
        assert len(self.tk._queue) == 1
        task = self.tk._queue.pop()
        assert task == Task("Destroy %s id %d" % (self.widget.name, w.id),
            { 'action':'destroy', 'id':w.id, })
        assert w.state == Control.DESTROYED
    
    def test_class(self):
        from rctk.widgets.control import Control
        w = self.create_widget()
        assert isinstance(w, Control)
    
    
class BaseNonRootWidgetTest(BaseWidgetTest):
    """
        Root is an odd case, this extended base class adds 
        tests for non-root widgets
    """
    def test_id(self):
        """ verify each widget gets a new id """

        def check(allocated, id):
            assert id not in allocated

        allocated = []
        for i in range(0, 5):
            id = self.create_widget().id
            ## the actual execution is deferred, make sure a copy is stored
            ## in stead of a reference, hence the [:] !
            yield check, allocated[:], id
            allocated.append(id)

    def test_id_nonzero(self):
        assert self.create_widget().id != 0
        
    
from rctk.widgets.button import Button
class TestButtonWidget(BaseNonRootWidgetTest):
    widget = Button

    def create_widget(self):
        return Button(self.tk, "hi")

from rctk.widgets.statictext import StaticText
class TestStaticTextWidget(BaseNonRootWidgetTest):
    widget = StaticText

    def create_widget(self):
        return StaticText(self.tk, "hi")

from rctk.widgets.text import Text
class TestTextWidget(BaseNonRootWidgetTest):
    widget = Text

    # test syncing value

from rctk.widgets.panel import Panel
class TestPanelWidget(BaseNonRootWidgetTest):
    widget = Panel

from rctk.widgets.checkbox import CheckBox
class TestCheckBoxWidget(BaseNonRootWidgetTest):
    widget = CheckBox

    # test syncing value

# from rctk.widgets.radiobutton import RadioButton
# class TestRadioButtonWidget(BaseNonRootWidgetTest):
#     widget = RadioButton
# 
#     # test setting group

from rctk.widgets.dropdown import Dropdown
class TestDropdownWidget(BaseNonRootWidgetTest):
    widget = Dropdown
    def create_widget(self):
        return self.widget(self.tk, ((1, 'a'), (2, 'b')))

    # test syncing selection, add()
    def test_items(self):
        w = self.create_widget()
        assert len(self.tk._queue) == 1
        assert self.tk._queue[0]._task['action'] == 'create'
        assert self.tk._queue[0]._task['control'] == self.widget.name
        assert self.tk._queue[0]._task['id'] == w.id
        assert 'items' in self.tk._queue[0]._task
        ## dropdown provides its own unique keys
        assert self.tk._queue[0]._task['items'] == [(0, 'a'), (1, 'b')]
        assert [(k, v) for (i, (k,v)) in w.items] == [(1, 'a'), (2, 'b')]
        

from rctk.widgets.list import List
class TestListWidget(TestDropdownWidget):
    widget = List

from rctk.widgets.window import Window
class TestWindowWidget(BaseNonRootWidgetTest):
    widget = Window
    def create_widget(self):
        return Window(self.tk, "window title")

from rctk.widgets.date import Date
class TestDateWidget(BaseNonRootWidgetTest):
    widget = Date

    # test syncing value

from rctk.widgets.text import Password
class TestPassword(BaseNonRootWidgetTest):
    widget = Password

from rctk.widgets.grid import Grid, Column
class TestWidget(BaseNonRootWidgetTest):
    widget = Grid

    def create_widget(self):
        return self.widget(self.tk, [Column('foo'), Column('bar')])

from rctk.widgets.root import Root
class TestRootCreate(BaseWidgetTest):
    """ 
        root is a special case. It doesn't result in a task (it's already 
        present by default) and always has id 0 (no matter how often created) 
    """
    widget = Root

    def test_create(self):
        root = self.create_widget()
        assert self.tk._queue == []

    def test_id(self):
        from rctk.widgets.root import Root

        root = self.create_widget()
        assert root.id == 0

    def test_id_zero(self):
        from rctk.widgets.root import Root

        def check(r):
            assert r.id == 0

        for i in range(0, 5):
            root = self.create_widget()
            yield check, root

import py.test

class TestImage(object): 
    def test_lies(self):
        py.test.skip("Niet goed getest")
