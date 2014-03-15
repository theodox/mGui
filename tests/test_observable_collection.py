'''
Created on Mar 14, 2014

@author: Stephen Theodore
'''
from unittest import TestCase
from mGui.observable import ObservableCollection, ViewCollection
from mGui.bindings import BindableObject

class TestTarget (BindableObject):
    _BIND_TGT = 'Values'
    
    def __init__(self):
        self.Values = []

class Test_ObservableCollection(TestCase):
    
    
    def test_base_binding(self):
        t = TestTarget()
        c = ObservableCollection(1,2,3,4,5,6,7,8,9,10)
        t << c
        t.update_bindings()
        assert t.Values == (1,2,3,4,5,6,7,8,9,10)
        
    def test_base_binding_auto_update_add(self):
        t = TestTarget()
        c = ObservableCollection(1,2,3,4,5,6,7,8,9,10)
        t << c
        c.add(11)
        assert t.Values == (1,2,3,4,5,6,7,8,9,10,11)

    def test_base_binding_auto_update_remove(self):
        t = TestTarget()
        c = ObservableCollection(1,2,3,4,5,6,7,8,9,10)
        t << c
        c.remove(5)
        assert t.Values == (1,2,3,4,6,7,8,9,10)

    def test_base_binding_force(self):
        t = TestTarget()
        c = ObservableCollection(1,2,3,4,5,6,7,8,9,10)
        t << c
        c._Internal_Collection = ['a','b','c']
        c.update_bindings()
        assert t.Values == ('a','b','c')

    def test_base_binding_clear(self):
        t = TestTarget()
        c = ObservableCollection(1,2,3,4,5,6,7,8,9,10)
        t << c
        c.update_bindings()
        assert t.Values == (1,2,3,4,5,6,7,8,9,10)
        c.clear()
        assert t.Values == ()
    
    def test_base_binding_sort(self):
        t = TestTarget()
        c = ObservableCollection(1,2,3,4,5,6,7,8,9,10)
        t << c
        c.update_bindings()
        assert t.Values == (1,2,3,4,5,6,7,8,9,10)
        c.sort(reverse=True)
        assert t.Values == (10,9,8,7,6,5,4,3,2,1)
    
    def test_iter(self):
        c = ObservableCollection(1,2,3,4,5,6,7,8,9,10)
        result = []
        for item in c: result.append(item)
        assert result == [1,2,3,4,5,6,7,8,9,10]

class TestObservableCollectionEvents(TestCase):
      
        class Tester(object):
            
            def __init__(self):
                self.Args = None
                self.Kwargs = None
            def handle_event(self, *args, **kwargs):
                self.Args = args
                self.Kwargs = kwargs
            
            
        def test_CollectionChanged_add(self):
            c = ObservableCollection(1,2,3,4,5,6,7,8,9,10)
            t = self.Tester()
            c.CollectionChanged += t.handle_event
            c.add(11)
            assert t.Kwargs['collection'] == c

        def test_CollectionChanged_remove(self):
            c = ObservableCollection(1,2,3,4,5,6,7,8,9,10)
            t = self.Tester()
            c.CollectionChanged += t.handle_event
            c.remove(1)
            assert t.Kwargs['collection'] == c

        def test_ItemAdded(self):
            c = ObservableCollection(1,2,3,4)
            t = self.Tester()
            c.ItemAdded += t.handle_event
            c.add(1)
            assert t.Kwargs['collection'] == c
            assert t.Args == (1,4)
            
        def test_ItemRemoved(self):
            c = ObservableCollection(1,2,3,4)
            t = self.Tester()
            c.ItemRemoved += t.handle_event
            c.remove(1)
            assert t.Kwargs['collection'] == c
            assert t.Args == (1,0)
        
        def test_Reordered(self):
            c = ObservableCollection(5,8,2)
            t = self.Tester()
            c.Reordered += t.handle_event
            c.sort(reverse=True)
            assert t.Kwargs['collection'] == c
            
        def test_ViewChanged (self):
            v = ViewCollection(5,8,2)
            t = self.Tester()
            v.ViewChanged += t.handle_event
            v.update_filter(lambda x : x < 5)
            assert t.Kwargs['collection'] == v
            
            
class TestViewCollection(TestCase):
    
    def test_base_binding(self):
        t = TestTarget()
        c = ViewCollection(1,2,3,4,5,6,7,8,9,10)
        t << c
        t.update_bindings()
        assert t.Values == (1,2,3,4,5,6,7,8,9,10)
        
    def test_base_binding_auto_update_add(self):
        t = TestTarget()
        c = ViewCollection(1,2,3,4,5,6,7,8,9,10)
        t << c
        c.add(11)
        assert t.Values == (1,2,3,4,5,6,7,8,9,10,11)

    def test_base_binding_auto_update_remove(self):
        t = TestTarget()
        c = ViewCollection(1,2,3,4,5,6,7,8,9,10)
        t << c
        c.remove(5)
        assert t.Values == (1,2,3,4,6,7,8,9,10)

    def test_base_binding_force(self):
        t = TestTarget()
        c = ViewCollection(1,2,3,4,5,6,7,8,9,10)
        t << c
        c._Internal_Collection = ['a','b','c']
        c.update_bindings()
        assert t.Values == ('a','b','c')

    def test_base_binding_clear(self):
        t = TestTarget()
        c = ViewCollection(1,2,3,4,5,6,7,8,9,10)
        t << c
        c.update_bindings()
        assert t.Values == (1,2,3,4,5,6,7,8,9,10)
        c.clear()
        assert t.Values == ()
    
    def test_base_binding_sort(self):
        t = TestTarget()
        c = ViewCollection(1,2,3,4,5,6,7,8,9,10)
        t << c
        c.update_bindings()
        assert t.Values == (1,2,3,4,5,6,7,8,9,10)
        c.sort(reverse=True)
        assert t.Values == (10,9,8,7,6,5,4,3,2,1)
    
    def test_iter(self):
        c = ViewCollection(1,2,3,4,5,6,7,8,9,10)
        result = []
        for item in c: result.append(item)
        assert result == [1,2,3,4,5,6,7,8,9,10]
        
    def test_filter(self):
        t = TestTarget()
        c = ViewCollection(1,2,3,4,5,6,7,8,9,10)
        t << c
        t.update_bindings()
        assert t.Values == (1,2,3,4,5,6,7,8,9,10)
        c.update_filter( lambda x: x % 2 == 0)
        assert t.Values == (2,4,6,8,10)
        
        
        