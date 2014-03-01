'''
Created on Mar 1, 2014

@author: Stephen Theodore
'''
import mGui.bindings as bindings
from unittest import TestCase


class Test_Accessors(TestCase):
    
    def setUp(self):
        bindings.BREAK_ON_BIND_FAILURE = False

    def test_dict_get(self):
        example = {'hello':'world'}
        ac = bindings.DictAccessor(example, 'hello')
        assert ac.pull() == 'world'
        
    def test_dict_set(self):
        example = {'hello':'world'}
        ac = bindings.DictAccessor(example, 'hello')
        ac.push('Las Vegas')
        assert example['hello'] == 'Las Vegas'


    def test_dict_raises(self):
        example = {'hello':'world'}
        ac = bindings.DictAccessor(example, 'i do not exist')
        bindings.BREAK_ON_BIND_FAILURE = True
        self.assertRaises(Exception, ac.pull)

    def test_dict_returns_empty_string_for_no_key(self):
        example = {'hello':'world'}
        ac = bindings.DictAccessor(example, 'i do not exist')
        bindings.BREAK_ON_BIND_FAILURE = False
        assert ac.pull() == ''

    def test_dict_set_does_not_raise(self):
        example = {'hello':'world'}
        ac = bindings.DictAccessor(example, 'i do not exist')
        bindings.BREAK_ON_BIND_FAILURE = True
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
        
        bindings.BREAK_ON_BIND_FAILURE = True
        test = object()
        ac = bindings.Accessor(test, 'xxx')
        self.assertRaises(Exception, ac.pull)

    def test_accessor_raises_no_field_set(self):
        
        bindings.BREAK_ON_BIND_FAILURE = True
        test = object()
        ac = bindings.Accessor(test, 'xxx')
        self.assertRaises(Exception, ac.push)
        
    def test_accessor_no_raise_when_suppressed(self):
        bindings.BREAK_ON_BIND_FAILURE = False
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
        sample._val == 888
        
                
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
        ac.push (val=888) 
        assert sample._val == 888
  
        