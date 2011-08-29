from rctk.widgets.control import Attribute, AttributeHolder
import py.test

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

    def test_initialization_simple(self):
        class A(AttributeHolder):
            a = Attribute('aa', Attribute.STRING)
            b = Attribute(31337, Attribute.NUMBER)
        t1 = A(a='bb', b=123)
        assert t1.a == 'bb'
        assert t1.b == 123

    def test_initialization_notused(self):
        class A(AttributeHolder):
            a = Attribute('aa', Attribute.STRING)
            b = Attribute(31337, Attribute.NUMBER)
        t1 = A(c='xyz')
        assert t1.a == 'aa'
        assert t1.b == 31337
        def test_c():
                t1.c == 'xyz'
        py.test.raises(AttributeError, test_c)

    def test_block_creation(self):
        class A(AttributeHolder):
            a = Attribute('aa', Attribute.STRING)
            def allow_update(self, name, value):
                return False

        ## test both methods of setting
        t = A()
        t.a = 'bb'
        assert t.a == 'aa'

        t2 = A(a='bb')
        assert t.a == 'aa'

    def test_block_creation_exception(self):
        class BlockException(Exception):
            pass

        class A(AttributeHolder):
            a = Attribute('aa', Attribute.STRING)
            def allow_update(self, name, value):
                raise BlockException("Don't!")

        t = A()
        def set_blocked():
            t.a = 'bb'

        ## test both methods of setting
        py.test.raises(BlockException, set_blocked)
        py.test.raises(BlockException, A, a='bb')

    def test_block_defaults(self):
        """ defaults are never blocked """
        class BlockException(Exception):
            pass

        class A(AttributeHolder):
            a = Attribute('aa', Attribute.STRING)
            def allow_update(self, name, value):
                raise BlockException("Don't!")

        t = A()
        assert t.a == 'aa'

    def test_callback(self):
        class A(AttributeHolder):
            a = Attribute('aa', Attribute.STRING)
            def __init__(self, **kw):
                self.changed_name = None
                self.changed_value = None
                super(A, self).__init__(**kw)

            def attribute_updated(self, name, value):
                self.changed_name = name
                self.changed_value = value

        t = A()
        t.a = 'bb'
        assert t.changed_value == 'bb'

        t2 = A(a='cc')
        assert t2.changed_value == 'cc'

    def test_callback_defaults(self):
        """ the callback is not invoked when setting defaults """
        class A(AttributeHolder):
            a = Attribute('aa', Attribute.STRING)
            def __init__(self, **kw):
                self.changed_name = None
                self.changed_value = None
                super(A, self).__init__(**kw)

            def attribute_updated(self, name, value):
                self.changed_name = name
                self.changed_value = value

        t = A()
        assert t.a == 'aa'
        assert t.changed_value == None

    def test_type_conversion_string(self):
        class A(AttributeHolder):
            a = Attribute("aa", Attribute.STRING)

        assert A.convert_from_xml("a", "123") == "123"
        assert A.convert_from_xml("a", "True") == "True"
        assert A.convert_from_xml("a", "foo bar") == "foo bar"

    def test_type_conversion_number(self):
        class A(AttributeHolder):
            a = Attribute("aa", Attribute.NUMBER)

        assert A.convert_from_xml("a", "123") == 123

    def test_type_conversion_boolean(self):
        class A(AttributeHolder):
            a = Attribute("aa", Attribute.BOOLEAN)

        assert A.convert_from_xml("a", "True") == True
        assert A.convert_from_xml("a", "true") == True
        assert A.convert_from_xml("a", "t") == True
        assert A.convert_from_xml("a", "1") == True
        assert A.convert_from_xml("a", "0") == False
        assert A.convert_from_xml("a", "false") == False
        assert A.convert_from_xml("a", "False") == False

    def test_required_attributes_none(self):
        class A(AttributeHolder):
            a = Attribute("aa", Attribute.BOOLEAN)

        assert A.required_attributes() == []

    def test_required_attributes_none(self):
        class A(AttributeHolder):
            a = Attribute("aa", Attribute.BOOLEAN)
            b = Attribute("bb", Attribute.BOOLEAN, required=True)

        assert A.required_attributes() == ["b"]

## test filtering?

## To be tested in control:
## - actual syncing (task generation)
## - don't allow updates on destroyed controls
## - don't generate tasks before creation
