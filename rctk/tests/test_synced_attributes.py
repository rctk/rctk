from rctk.widgets.control import Attribute, AttributeHolder

class TestSyncedAttributes(object):
    def test_trivial(self):
        class T(AttributeHolder):
            title = Attribute('default', Attribute.STRING)
        t = T()
        assert t.title == 'default'
        t.title = '123'
        assert t.title == '123'
        assert 'title' in t.attributes()
        assert t.attributes()['title'].type == Attribute.STRING

    def test_unique(self):
        """ make sure attributes are not shared """
        class T(AttributeHolder):
            title = Attribute('default', Attribute.STRING)
        t1, t2 = T(), T()
        t1.title = 'different'
        assert t2.title == 'default'

    def test_inherited(self):
        class A(AttributeHolder):
            a = Attribute('aa', Attribute.STRING)
        class B(A):
            b = Attribute('bb', Attribute.STRING)

        b = B()
        assert b.a == 'aa'
        assert b.b == 'bb'
        b.a = 'aaa'
        b.b = 'bbb'
        assert b.a == 'aaa'
        assert b.b == 'bbb'
        assert 'a' in b.attributes()
        assert 'b' in b.attributes()

    def test_override(self):
        class A(AttributeHolder):
            a = Attribute('aa', Attribute.STRING)
        class B(A):
            a = Attribute('bb', Attribute.STRING)
        b = B()
        assert b.a == 'bb'

## test not-syncing before creation, explicit syncing after creation,
## not-syncing destroyed controls.

