'''
Created on Mar 1, 2014

@author: Stephen Theodore
'''
import mock_maya
import mGui.bindings as bindings
from unittest import TestCase
import maya.cmds as cmds
#import pymel.core as pm


class Test_Accessors(TestCase):
    def setUp(self):
        bindings.BREAK_ON_BIND_FAILURE = False
        bindings.BREAK_ON_ACCESS_FAILURE = True

    def tearDown(self):
        bindings.BREAK_ON_BIND_FAILURE = False
        bindings.BREAK_ON_ACCESS_FAILURE = True

    def test_dict_get(self):
        example = {'hello': 'world'}
        ac = bindings.DictAccessor(example, 'hello')
        assert ac.pull() == 'world'

    def test_dict_set(self):
        example = {'hello': 'world'}
        ac = bindings.DictAccessor(example, 'hello')
        ac.push('Las Vegas')
        assert example['hello'] == 'Las Vegas'

    def test_dict_raises(self):
        example = {'hello': 'world'}
        ac = bindings.DictAccessor(example, 'i do not exist')
        bindings.BREAK_ON_ACCESS_FAILURE = True
        self.assertRaises(Exception, ac.pull)

    def test_dict_returns_zero_for_no_key(self):
        example = {'hello': 'world'}
        ac = bindings.DictAccessor(example, 'i do not exist')
        bindings.BREAK_ON_ACCESS_FAILURE = False
        assert ac.pull() == 0

    def test_dict_set_does_not_raise(self):
        example = {'hello': 'world'}
        ac = bindings.DictAccessor(example, 'i do not exist')
        bindings.BREAK_ON_ACCESS_FAILURE = True
        ac.push(True)
        assert example['i do not exist']

    def test_accessor_get_field(self):
        import datetime
        test = datetime.datetime.now()
        ac = bindings.Accessor(test, 'year')
        assert ac.pull() == datetime.datetime.now().year

    def test_accessor_get_property(self):

        class Dummy(object):
            @property
            def test_prop(self):
                return 999

        sample = Dummy()
        ac = bindings.Accessor(sample, 'test_prop')
        assert ac.pull() == 999

    def test_accessor_set_field(self):
        class Dummy(object):
            def __init__(self):
                self.Field = 'green'

        sample = Dummy()
        ac = bindings.Accessor(sample, 'Field')
        ac.push('brown')
        assert sample.Field == 'brown'

    def test_accessor_set_property(self):

        class Dummy(object):
            def __init__(self):
                self._val = 999

            @property
            def test_prop(self):
                return self._val

            @test_prop.setter
            def test_prop(self, val):
                self._val = val

        sample = Dummy()
        ac = bindings.Accessor(sample, 'test_prop')
        ac.push(888)
        assert sample.test_prop == 888
        assert ac.pull() == 888

    def test_accessor_raises_no_field(self):

        bindings.BREAK_ON_ACCESS_FAILURE = True
        test = object()
        ac = bindings.Accessor(test, 'xxx')
        self.assertRaises(Exception, ac.pull)

    def test_accessor_raises_no_field_set(self):

        bindings.BREAK_ON_ACCESS_FAILURE = True
        test = object()
        ac = bindings.Accessor(test, 'xxx')
        self.assertRaises(Exception, ac.push)

    def test_accessor_no_raise_when_suppressed(self):
        bindings.BREAK_ON_ACCESS_FAILURE = False
        test = object()
        ac = bindings.Accessor(test, 'xxx')
        ac.pull()
        ac.push()

    def test_method_accessor_simple(self):
        class Dummy(object):
            def __init__(self):
                self._val = 999

            def get_val(self):
                return self._val

        sample = Dummy()
        ac = bindings.MethodAccessor(sample, 'get_val')
        assert ac.pull() == 999

    def test_method_accessor_args(self):
        class Dummy(object):
            def __init__(self):
                self._val = 999

            def get_val(self, doit):
                if doit == 888:
                    return self._val

        sample = Dummy()
        ac = bindings.MethodAccessor(sample, 'get_val')
        assert ac.pull(888) == 999

    def test_method_accessor_kwargs(self):
        class Dummy(object):
            def __init__(self):
                self._val = 999

            def get_val(self, **kwargs):
                if kwargs['doit'] == 888:
                    return self._val

        sample = Dummy()
        ac = bindings.MethodAccessor(sample, 'get_val')
        assert ac.pull(doit=888) == 999

    def test_method_accessor_set_simple(self):
        class Dummy(object):
            def __init__(self):
                self._val = 999

            def get_val(self):
                return self._val

            def set_val(self, val):
                self._val = val

        sample = Dummy()
        ac = bindings.MethodAccessor(sample, 'set_val')
        ac.push(888)
        assert sample._val == 888

    def test_method_accessor_set_args(self):
        class Dummy(object):
            def __init__(self):
                self._val = 999

            def get_val(self, doit):
                if doit == 888:
                    return self._val

            def set_val(self, *args):
                self._val = args[0]

        sample = Dummy()
        ac = bindings.MethodAccessor(sample, 'set_val')
        ac.push(777)
        assert sample._val == 777

    def test_method_accessor_kwargs_set(self):

        class Dummy(object):
            def __init__(self):
                self._val = 999

            def set_val(self, **kwargs):
                self._val = kwargs['val']

        sample = Dummy()
        ac = bindings.MethodAccessor(sample, 'set_val')
        ac.push(val=888)
        assert sample._val == 888

    def test_cmds_accessor_get(self):
        cmds.file(new=True, f=True)
        cmds.polyCube.side_effect= [('pCube1', 'polyCube1')]
        test_obj, _ = cmds.polyCube()
        cmds.xform(test_obj, rotation=(10, 10, 10))
        cmds.xform.side_effect = [(10,10,10)]
        ac = bindings.CmdsAccessor(test_obj, 'r')
        assert ac.pull() == [(10, 10, 10)]

    def test_cmds_accessor_set(self):
        cmds.file(new=True, f=True)
        ac = bindings.CmdsAccessor('front', 'tz')
        ac.push(55)
        assert cmds.setAttr.called_with('front.tz', q=True)
#        assert cmds.getAttr('front.tz') == 55

    # def test_py_accessor_get(self):
    #     cmds.file(new=True, f=True)
    #     test_obj, _ = cmds.polyCube()
    #     pynode = pm.PyNode(test_obj)
    #     ac = bindings.PyNodeAccessor(pynode, 'rx')
    #     assert ac.pull() == 0

    # def test_py_accessor_set(self):
    #     cmds.file(new=True, f=True)
    #     front = pm.PyNode('front')
    #     ac = bindings.PyNodeAccessor(front, 'rx')
    #     ac.push(55)
    #     assert front.attr('rx').get() == 55

    # def test_py_attrib_accessor_get(self):
    #     cmds.file(new=True, f=True)
    #     front = pm.PyNode('front')
    #     ac = bindings.PyAttributeAccessor(front.rx, None)
    #     ac.push(55)
    #     assert front.attr('rx').get() == 55

    # def test_py_attrib_accessor_set(self):
    #     cmds.file(new=True, f=True)
    #     front = pm.PyNode('front')
    #     ac = bindings.PyAttributeAccessor(front.rx, None)
    #     ac.push(55)
    #     assert front.attr('rx').get() == 55


class TestAccessorFactory(TestCase):
    def test_find_simple_property(self):
        class Dummy(object):
            def __init__(self):
                self.Property = 999

        sample = Dummy()
        accessor = bindings.get_accessor(sample, 'Property')
        assert isinstance(accessor, bindings.Accessor)
        assert accessor.pull() == 999

    def test_find_mapped_property(self):
        sample = {'hello': 'world'}
        accessor = bindings.get_accessor(sample, 'hello')
        assert isinstance(accessor, bindings.DictAccessor)
        assert accessor.pull() == 'world'

    def test_find_mapped_on_mapping_derived(self):

        class MapTest(object):
            def __init__(self):
                self.secret = 999

            def __getitem__(self, key):
                if key == 'test':
                    return self.secret
                else:
                    return -999

            def __setitem__(self, key, val):
                if key == 'test': self.secret = val

            def __len__(self):
                return 1

        example = MapTest()
        accessor = bindings.get_accessor(example, 'test')
        assert isinstance(accessor, bindings.DictAccessor)
        assert accessor.pull() == 999

    def test_cmds_accessor(self):
        cmds.file(new=True, f=True)

        ac = bindings.get_accessor('persp', 'tx')
        assert isinstance(ac, bindings.CmdsAccessor)

    def test_cmds_accessor_excepts_for_nonexistent_object(self):
        cmds.file(new=True, f=True)
        self.assertRaises(bindings.BindingError, lambda: bindings.get_accessor('dont_exist', 'tx'))

    def test_cmds_accessor_excepts_for_nonexistent_attrrib(self):
        cmds.file(new=True, f=True)
        self.assertRaises(bindings.BindingError, lambda: bindings.get_accessor('persp', 'dontexist'))

    # def test_pynode_accessor(self):
    #     cmds.file(new=True, f=True)
    #     cube, shape = pm.polyCube()
    #     ac = bindings.get_accessor(cube, 'rx')
    #     assert isinstance(ac, bindings.PyNodeAccessor)
    #     ac2 = bindings.get_accessor(shape, 'width')
    #     assert isinstance(ac2, bindings.PyNodeAccessor)

    # def test_pynode_accessor_excepts_for_nonexistent_attrib(self):
    #     cmds.file(new=True, f=True)
    #     cube, _ = pm.polyCube()
    #     self.assertRaises(bindings.BindingError, lambda: bindings.get_accessor(cube, 'xyz'))

    # def test_pyattr_accessor(self):
    #     cmds.file(new=True, f=True)
    #     cube, shape = pm.polyCube()
    #     ac = bindings.get_accessor(cube.rx)
    #     assert isinstance(ac, bindings.PyAttributeAccessor)
    #     ac2 = bindings.get_accessor(shape.width)
    #     assert isinstance(ac2, bindings.PyAttributeAccessor)


class TestBindings(TestCase):
    class Example(object):
        def __init__(self, name, val):
            self.name = name
            self.val = val

    def setUp(self):
        bindings.BREAK_ON_BIND_FAILURE = False
        bindings.BREAK_ON_ACCESS_FAILURE = True

    def tearDown(self):
        bindings.BREAK_ON_BIND_FAILURE = False
        bindings.BREAK_ON_ACCESS_FAILURE = True

    def test_basic_binding(self):
        ex = self.Example('fred', 'flintstone')
        ex2 = self.Example('barney', 'rubble')
        tester = bindings.Binding(bindings.get_accessor(ex, 'name'), bindings.get_accessor(ex2, 'val'))
        assert tester

    def test_basic_binding_update(self):
        ex = self.Example('fred', 'flintstone')
        ex2 = self.Example('barney', 'rubble')
        tester = bindings.Binding(bindings.get_accessor(ex, 'name'), bindings.get_accessor(ex2, 'val'))
        tester()
        assert ex2.val == ex.name

    def test_binding_source_order(self):
        ex = self.Example('fred', 'flintstone')
        ex2 = self.Example('barney', 'rubble')
        tester = bindings.Binding(bindings.get_accessor(ex, 'name'), bindings.get_accessor(ex2, 'val'))
        assert tester.getter.target.name == 'fred'
        assert tester.setter.target.name == 'barney'

    def test_binding_survives_object_deletion(self):
        ex = self.Example('fred', 'flintstone')
        ex2 = self.Example('barney', 'rubble')
        tester = bindings.Binding(bindings.get_accessor(ex, 'name'), bindings.get_accessor(ex2, 'val'))
        del (ex)
        assert not tester()  # deleted referent = failed binding
        assert ex2.val == 'rubble'  # so value is unchanged

    def test_bindings_except_when_allowed(self):
        ex = self.Example('fred', 'flintstone')
        ex2 = self.Example('barney', 'rubble')
        tester = bindings.Binding(bindings.get_accessor(ex, 'name'), bindings.get_accessor(ex2, 'val'))
        bindings.BREAK_ON_ACCESS_FAILURE = True
        bindings.BREAK_ON_BIND_FAILURE = True
        del (ex)
        self.assertRaises(bindings.BindingError, tester)

    def test_binding_excepts_on_bad_arguments(self):
        self.assertRaises(bindings.BindingError, lambda: bindings.Binding(None, None))

    def test_invalidate(self):
        ex = self.Example('fred', 'flintstone')
        ex2 = self.Example('barney', 'rubble')
        tester = bindings.Binding(bindings.get_accessor(ex, 'name'), bindings.get_accessor(ex2, 'val'))
        tester.invalidate()
        assert not tester

    def test_invalid_binding_fails(self):
        ex = self.Example('fred', 'flintstone')
        ex2 = self.Example('barney', 'rubble')
        tester = bindings.Binding(bindings.get_accessor(ex, 'name'), bindings.get_accessor(ex2, 'val'))
        tester.invalidate()
        assert not tester()


class TestBindable(TestCase):
    class Example(bindings.Bindable):
        def __init__(self, name, val):
            self.name = name
            self.val = val

    def test_bindable_bind_to(self):
        ex = self.Example('fred', 'flintstone')
        ex2 = self.Example('barney', 'rubble')
        test = ex & "name" > bindings.bind() > (ex2, 'val')
        assert isinstance(test, bindings.Binding)
        assert test
        test()
        assert ex2.val == ex.name

    def test_bindable_bind_from(self):
        ex = self.Example('fred', 'flintstone')
        ex2 = self.Example('barney', 'rubble')
        test = ex & "name" < bindings.bind() < (ex2, 'val')
        assert isinstance(test, bindings.Binding)
        assert test
        test()
        assert ex.name == ex2.val

    def test_bindable_plus(self):
        ex = self.Example('fred', 'flintstone')
        tester = ex & 'val'
        assert tester.item == ex
        assert tester.attribute == 'val'

    def test_bind_to_cmds_string(self):
        ex = self.Example('cube', 45)
        cmds.file(new=True, f=True)
        cmds.polyCube()
        tester = ex & 'val' > bindings.bind() > ('pCube1', 'tx')
        tester()
        assert cmds.getAttr('pCube1.tx') == 45
        tester2 = ex & 'val' > bindings.bind() > 'pCube1.ty'
        tester2()
        assert cmds.getAttr('pCube1.ty') == 45

    # def test_bind_to_pyAttr(self):
    #     ex = self.Example('cube', 45)
    #     cmds.file(new=True, f=True)
    #     cube, shape = pm.polyCube()
    #     tester = ex & 'val' > bindings.bind() > cube.tx
    #     tester()
    #     assert cmds.getAttr('pCube1.tx') == 45

    # def test_bind_to_pyNode(self):
    #     ex = self.Example('cube', 45)
    #     cmds.file(new=True, f=True)
    #     cube, shape = pm.polyCube()
    #     tester = ex & 'val' > bindings.bind() > (cube, 'tx')
    #     tester()
    #     assert cmds.getAttr('pCube1.tx') == 45


class TestBindableObject(TestCase):
    class Example(bindings.BindableObject):
        _BIND_SRC = 'name'
        _BIND_TGT = 'val'

        def __init__(self, name, val):
            self.name = name
            self.val = val

    def test_default_src(self):
        ex = self.Example('fred', 'flinstone')
        assert ex.bind_source == 'name'

    def test_default_tgt(self):
        ex = self.Example('fred', 'flinstone')
        assert ex.bind_target == 'val'

    def test_default_bindings(self):
        ex1 = self.Example('fred', 'flintstone')
        ex2 = self.Example('barney', 'rubble')
        tester = ex1 > bindings.bind() > ex2
        tester()
        assert ex2.val == ex1.name
        tester = ex1 < bindings.bind() < ex2
        tester()
        assert ex1.val == ex2.name

    def test_override_default_bindings(self):
        ex1 = self.Example('fred', 'flintstone')
        ex2 = self.Example('barney', 'rubble')
        tester = ex1 & 'val' > bindings.bind() > ex2 & 'name'
        tester()
        assert ex2.name == ex1.val

    def text_mix_default_and_non_default_bindings(self):
        ex1 = self.Example('fred', 'flintstone')
        ex2 = {'pebbles': 'bambam'}
        tester = ex1 > bindings.bind() > ex2 & 'pebbles'
        tester()
        assert ex2['pebbles'] == 'fred'


class Test_BindProxy(TestCase):
    def test_bindproxy_site(self):
        b = bindings.BindProxy('persp', 'ty')
        assert b.item == 'persp'

    def test_bindproxy_dict(self):
        b = bindings.BindProxy({'hello': 'world'}, 'hello')
        assert b.item['hello'] == 'world'

    def test_bindproxy_site_nesting(self):
        class Example(bindings.BindableObject):
            _BIND_SRC = 'name'
            _BIND_TGT = 'val'

            def __init__(self, name, val):
                self.name = name
                self.val = val

        ex = Example('fred', 'flintstone')
        test = bindings.BindProxy(ex, 'val')
        assert test.item is ex


class TestBindingCollection(TestCase):
    def setUp(self):
        bindings.BREAK_ON_BIND_FAILURE = False
        bindings.BREAK_ON_ACCESS_FAILURE = True

    def tearDown(self):
        bindings.BREAK_ON_BIND_FAILURE = False
        bindings.BREAK_ON_ACCESS_FAILURE = True

    class Example(bindings.BindableObject):
        _BIND_SRC = 'name'
        _BIND_TGT = 'val'

        def __init__(self, name, val):
            self.name = name
            self.val = val

    def test_binding_collection_auto_update_defaults_on(self):
        fred = self.Example('fred', 'flintstone')
        barney = self.Example('barney', 'rubble')
        wilma = self.Example('wilma', None)
        bambam = self.Example('bambam', None)
        guys = {'fred': None, 'barney': None}
        with bindings.BindingContext() as ctx:
            fred & 'val' > bindings.bind() > wilma  # default target
            barney & 'val' > bindings.bind() > bambam & 'val'
            fred > bindings.bind() > (guys, 'fred')  # default sources
            barney > bindings.bind() > (guys, 'barney')

        assert len(ctx.bindings) == 4
        assert wilma.val == 'flintstone'
        assert bambam.val == 'rubble'
        assert guys == {'fred': 'fred', 'barney': 'barney'}

    def test_binding_collection_auto_update_suppress(self):
        fred = self.Example('fred', 'flintstone')
        barney = self.Example('barney', 'rubble')
        wilma = self.Example('wilma', None)
        bambam = self.Example('bambam', None)
        guys = {'fred': None, 'barney': None}
        with bindings.BindingContext(auto_update=False) as ctx:
            fred & 'val' > bindings.bind() > wilma  # default target
            barney & 'val' > bindings.bind() > bambam & 'val'
            fred > bindings.bind() > (guys, 'fred')  # default sources
            barney > bindings.bind() > (guys, 'barney')
        assert len(ctx.bindings) == 4
        assert wilma.val == None
        assert bambam.val == None
        assert guys == {'fred': None, 'barney': None}

    def test_collection_deletes_bad_bindings(self):
        fred = self.Example('fred', 'flintstone')
        barney = self.Example('barney', 'rubble')
        wilma = self.Example('wilma', None)
        bambam = self.Example('bambam', None)
        guys = {'fred': None, 'barney': None}
        with bindings.BindingContext(False) as ctx:
            fred & 'val' > bindings.bind() > wilma  # default target
            barney & 'val' > bindings.bind() > bambam & 'val'
            fred > bindings.bind() > (guys, 'fred')  # default sources
            barney > bindings.bind() > (guys, 'barney')
            del (fred)  # delete referent invalidating 2 bindings
        ctx.update()
        assert len(ctx.bindings) == 2
        assert wilma.val is None
        assert guys['fred'] is None

    def test_collection_hierarchy(self):
        fred = self.Example('fred', 'flintstone')
        barney = self.Example('barney', 'rubble')
        wilma = self.Example('wilma', None)
        bambam = self.Example('bambam', None)
        guys = {'fred': None, 'barney': None}
        with bindings.BindingContext(auto_update=False) as outer:
            _ = fred & 'val' > bindings.bind() > wilma
            with bindings.BindingContext(auto_update=False) as middle:
                _ = barney & 'val' > bindings.bind() > bambam & 'val'
                with bindings.BindingContext(auto_update=False) as ctx:
                    _ = fred > bindings.bind() > (guys, 'fred')  # default sources
                    _ = barney > bindings.bind() > (guys, 'barney')

        outer.update()
        assert wilma.val == 'flintstone'
        assert bambam.val == 'rubble'
        assert guys == {'fred': 'fred', 'barney': 'barney'}

    def test_collection_hierarchy_does_not_recurse_automatically(self):
        fred = self.Example('fred', 'flintstone')
        barney = self.Example('barney', 'rubble')
        wilma = self.Example('wilma', None)
        bambam = self.Example('bambam', None)
        guys = {'fred': None, 'barney': None}
        with bindings.BindingContext(auto_update=True) as outer:
            fred & 'val' > bindings.bind() > wilma
            with bindings.BindingContext(auto_update=False) as middle:
                barney & 'val' > bindings.bind() > bambam & 'val'
                with bindings.BindingContext(auto_update=False) as ctx:
                    fred > bindings.bind() > (guys, 'fred')  # default sources
                    barney > bindings.bind() > (guys, 'barney')

        assert wilma.val == 'flintstone'
        assert not bambam.val == 'rubble'
        assert not guys == {'fred': 'fred', 'barney': 'barney'}

    def test_collection_hierarchy_control_recursion(self):
        fred = self.Example('fred', 'flintstone')
        barney = self.Example('barney', 'rubble')
        wilma = self.Example('wilma', None)
        bambam = self.Example('bambam', None)
        guys = {'fred': None, 'barney': None}
        with bindings.BindingContext(auto_update=False) as outer:
            fred & 'val' > bindings.bind() > wilma
            with bindings.BindingContext(auto_update=False) as middle:
                barney & 'val' > bindings.bind() > bambam & 'val'
                with bindings.BindingContext(auto_update=False) as ctx:
                    fred > bindings.bind() > (guys, 'fred')  # default sources
                    barney > bindings.bind() > (guys, 'barney')

        outer.update(False)
        middle.update(False)
        assert wilma.val == 'flintstone'
        assert bambam.val == 'rubble'
        assert not guys == {'fred': 'fred', 'barney': 'barney'}


class TestTwoWayBinding(TestCase):
    class Example(bindings.BindableObject):
        _BIND_SRC = 'name'
        _BIND_TGT = 'val'

        def __init__(self, name, val):
            self.name = name
            self.val = val

    def test_two_way_assignment(self):
        fred = self.Example('fred', 'flintstone')
        barney = self.Example('barney', 'rubble')

        test = fred.bind.name | bindings.bind() | barney.bind.val
        barney.val = 'new'
        test()
        assert fred.name == barney.val and barney.val == 'new'

        fred.name = 'new2'
        test()
        assert fred.name == barney.val and fred.name == 'new2'
