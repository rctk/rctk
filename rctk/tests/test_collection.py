# test_collection.py

from rctk.tests.base import BaseTest
from rctk.widgets import StaticText


class BaseCollectionTest(BaseTest):
    """ Test basic collection behaviour. """
    item = StaticText
    collection = None
    
    def create_collection(self):
        return self.collection(self.tk, self.item)
    
    def test_empty(self):
        c = self.create_collection()
        assert len(c._items) == 0
        assert len(c._controls) == 0
    
    def test_append(self):
        c = self.create_collection()
        c.append('Foo')
        assert len(c._items) == 1
        assert len(c._controls) == 1
    
    def test_remove(self):
        c = self.create_collection()
        c.append('Foo')
        c.remove('Foo')
        assert len(c._items) == 0
        assert len(c._controls) == 0
    
    def test_extend(self):
        c = self.create_collection()
        c.extend(['Foo', 'Bar'])
        assert len(c._items) == 2
        assert len(c._controls) == 2
    
    def test_clear(self):
        c = self.create_collection()
        c.extend(['Foo', 'Bar'])
        c.clear()
        assert len(c._items) == 0
        assert len(c._controls) == 0

    
from portal.ui.collection import Collection
class  TestCollectionWidget(BaseCollectionTest):
    collection = Collection
