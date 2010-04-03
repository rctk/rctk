from rctk.toolkit import Toolkit
import simplejson

# http://codespeak.net/py/0.9.2/test.html
# http://agiletesting.blogspot.com/2005/01/python-unit-testing-part-3-pytest-tool.html
# pytest.org

def build_task_queue(method, type, id, **data):
    return simplejson.dumps([dict(method=method, type=type, id=id, data=data)])

class DummyApp(object):
    pass

class TestToolkit(Toolkit):
    def clear(self):
        self._queue = []

class BaseTest(object):
    def setup_method(self, method):
        self.tk = TestToolkit(DummyApp)
