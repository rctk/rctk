from rctk.tests.base import BaseTest, build_task_queue

class ClickCounter(object):
    def __init__(self):
        self.count = 0
        self.lastcontrol = None

    def __call__(self, event):
        self.lastcontrol = event.control
        self.count += 1

from rctk.event import Clickable

class BaseClickableTest(BaseTest):
    widget = None

    ## overlap with test_controls
    def create_widget(self):
        return self.widget(self.tk)

    def test_class(self):
        w = self.create_widget()
        assert isinstance(w, Clickable)

    def test_click_task(self):
        c = ClickCounter()
        w = self.create_widget()
        self.tk.clear() ## clear create event
        w.click = lambda event: None
        assert len(self.tk._queue) == 1
        assert self.tk._queue[0]._task['action'] == 'handler'
        assert self.tk._queue[0]._task['type'] == 'click'
        assert self.tk._queue[0]._task['control'] == self.widget.name
        assert self.tk._queue[0]._task['id'] == w.id

    def test_click(self):
        c = ClickCounter()
        w = self.create_widget()
        w.click = c
        assert c.count == 0

        ## simulate a remote click event
        self.tk.handle("task", queue=build_task_queue("event", type="click", id=w.id))

        assert c.count == 1
        assert c.lastcontrol == w


##
## Slight overlap with test_controls

from rctk.widgets.button import Button
class TestClickableButton(BaseClickableTest):
    widget = Button
    def create_widget(self):
        return self.widget(self.tk, "hi")

from rctk.widgets.checkbox import CheckBox
class TestClickableCheckBox(BaseClickableTest):
    widget = CheckBox

#from rctk.widgets.radiobutton import RadioButton
#class TestClickableRadioButton(BaseClickableTest):
#    widget = RadioButton
#    def create_widget(self):
#        return self.widget(self.tk, "hi")

from rctk.widgets.dropdown import Dropdown
class TestClickableDropdown(BaseClickableTest):
    widget = Dropdown

    def create_widget(self):
        return self.widget(self.tk, ((1, 'a'), (2, 'b')))

    ## verify a click receives the selection made

from rctk.widgets.list import List
class TestClickableList(TestClickableDropdown):
    widget = List

