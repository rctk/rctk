from rctk.task import Task

class TestTask(object):
    def test_equal(self):
        assert Task('foo', {'action': 'bar'}) == Task('foo', {'action': 'bar'})
    

