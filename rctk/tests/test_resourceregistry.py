class BaseTestResource(object):
    """ test individual resources and their behaviour """
    type = None

    def factory(self, **kw):
        return self.type(**kw)

    def test_naming(self):
        r = self.factory()
        assert r.name is not None

    def test_timestamp(self):
        """ a resource always has a timestamp """
        r = self.factory()

        assert r.timestamp is not None

    def test_type(self):
        """ a resource always has a type """
        r = self.factory()

        assert r.type is not None

    def test_duplicate_naming(self):
        """ resources can have the same name. """
        r1 = self.factory(name="foo")
        r2 = self.factory(name="foo")

        assert r1.name == r2.name

class TestBaseResource(BaseTestResource):
    from rctk.resourceregistry import BaseResource
    type = BaseResource

    def factory(self, data="", **kw):
        return self.type(data, **kw)

    def test_unique_name_generation(self):
        r1 = self.factory()
        r2 = self.factory()
        
        assert r1.name != r2.name

    def test_equality(self):
        r1 = self.factory(data="1")
        r2 = self.factory(data="1")

        assert r1 == r2

    def test_inequality(self):
        r1 = self.factory(data="1")
        r2 = self.factory(data="2")

        assert r1 != r2

class TestFileResource(BaseTestResource):
    from rctk.resourceregistry import FileResource
    type = FileResource

    def factory(self, path="files/dummy.x", **kw):
        return self.type(path, **kw)

    def test_equality(self):
        r1 = self.factory("files/dummy.x")
        r2 = self.factory("files/dummy.x")

        assert r1 == r2

    def test_inequality(self):
        r1 = self.factory("files/dummy.x")
        r2 = self.factory("files/dummy.y")
        r3 = self.factory("files/dummy.xx")

        # r3 has the same content as r1, still it's different
        assert r1 != r2
        assert r1 != r3
        assert r2 != r3

    def test_resolving(self):
        """ verify files are loaded relative to the calling module """
        r1 = self.factory("files/dummy.x")

        import os
        assert r1.path.startswith(os.path.dirname(__file__))

    def test_timestamp_found(self):
        import time
        now = time.time()

        ## a generated timestamp would be >= now
        r1 = self.factory("files/dummy.x")
        assert r1.timestamp < now

    def test_generated_name(self):
        r1 = self.factory("files/dummy.x")

        assert r1.name == "dummy.x"

class TestDynamicResource(BaseTestResource):
    from rctk.resourceregistry import DynamicResource
    type = DynamicResource

    class DummyDynamicResource(DynamicResource):
        def __call__(self, elements):
            return elements[-1]

    def test_dynamic_resource(self):
        r = TestDynamicResource.DummyDynamicResource()
        assert r(['a', 'b', 'c']) == 'c' 
        assert r(['a', 'b']) == 'b' 


class TestResourceRegistry(object):
    def setup_method(self, method):
        from rctk.resourceregistry import ResourceRegistry
        self.rr = ResourceRegistry()

    def test_order(self):
        """ assert that add-order is preserved """
        from rctk.resourceregistry import BaseResource
        r1 = BaseResource("3", name="c")
        r2 = BaseResource("2", name="a")
        r3 = BaseResource("1", name="b")

        self.rr.add(r1)
        self.rr.add(r2)
        self.rr.add(r3)

        assert self.rr.names() == ["c", "a", "b"]

    def test_duplicates(self):
        """ duplicates are not added """
        from rctk.resourceregistry import BaseResource
        r1 = BaseResource("1", name="foo")
        r2 = BaseResource("1", name="foo")

        self.rr.add(r1)
        self.rr.add(r2)

        assert len(self.rr.names()) == 1

    def test_duplicate_named_resource(self):
        from rctk.resourceregistry import BaseResource
        r1 = BaseResource("x", name="foo")
        r2 = BaseResource("y", name="foo")

        n1 = self.rr.add(r1)
        n2 = self.rr.add(r2)

        assert n1 != n2 

    def test_retrieve_resource(self):
        from rctk.resourceregistry import BaseResource
        r1 = BaseResource("x", name="foo")
        r2 = BaseResource("y", name="foo")

        n1 = self.rr.add(r1)
        n2 = self.rr.add(r2)

        assert self.rr.get_resource(n1).data == r1.data
        assert self.rr.get_resource(n2).data == r2.data

    def test_singleton(self):
        from rctk.resourceregistry import getResourceRegistry

        rr1 = getResourceRegistry()
        rr2 = getResourceRegistry()

        assert rr1 is rr2

class TestDynamicResourceInRegistry(object):
    def setup_method(self, method):
        from rctk.resourceregistry import ResourceRegistry
        self.rr = ResourceRegistry()

    from rctk.resourceregistry import DynamicResource
    class DummyDynamicResource(DynamicResource):
        def __call__(self, elements):
            return elements[-1]

    def test_equality(self):
        """
           two dynamic resources with the same name get different registrations
        """
        r1 = self.DummyDynamicResource("unique")
        r2 = self.DummyDynamicResource("unique")
        n1 = self.rr.add(r1)
        n2 = self.rr.add(r2)
        assert n1 != n2

    def test_dynamics(self):
        r = self.DummyDynamicResource("name")
        n = self.rr.add(r)
        assert self.rr.get_resource(n, ['a', 'b', 'c']) == 'c'
        assert self.rr.get_resource(n, ['a', 'b', ]) == 'b'


