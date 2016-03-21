'''
Created on Mar 14, 2014

@author: Stephen Theodore
'''
from mGui.bindings import BindableObject, bind
from mGui.observable import ObservableCollection, ViewCollection, ImmediateObservableCollection
from unittest import TestCase


class TestTarget(BindableObject):
    _BIND_TGT = 'values'

    def __init__(self):
        self.values = []


class Test_ObservableCollection(TestCase):
    def test_base_binding(self):
        t = TestTarget()
        c = ObservableCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t < bind() < c
        t.update_bindings()
        assert t.values == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    def test_base_binding_auto_update_add(self):
        t = TestTarget()
        c = ObservableCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t < bind() < c
        c.add(11)
        assert t.values == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)

    def test_base_binding_auto_update_remove(self):
        t = TestTarget()
        c = ObservableCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t < bind() < c
        c.remove(5)
        assert t.values == (1, 2, 3, 4, 6, 7, 8, 9, 10)

    def test_base_binding_force(self):
        t = TestTarget()
        c = ObservableCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t < bind() < c
        c._internal_collection = ['a', 'b', 'c']  # don't do this in practice!
        c.update_bindings()
        assert t.values == ('a', 'b', 'c')

    def test_base_binding_clear(self):
        t = TestTarget()
        c = ImmediateObservableCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t < bind() < c
        c.update_bindings()
        assert t.values == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        c.clear()
        assert t.values == ()

    def test_base_binding_sort(self):
        t = TestTarget()
        c = ImmediateObservableCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t < bind() < c
        c.update_bindings()
        assert t.values == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        c.sort(reverse=True)
        assert t.values == (10, 9, 8, 7, 6, 5, 4, 3, 2, 1)

    def test_iter(self):
        c = ImmediateObservableCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        result = []
        for item in c: result.append(item)
        assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


class TestObservableCollectionEvents(TestCase):
    class Tester(object):
        def __init__(self):
            self.args = None
            self.kwargs = None
            self.has_fired = False

        def handle_event(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            self.has_fired = True

    def test_onCollectionChanged_add(self):
        c = ImmediateObservableCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t = self.Tester()
        c.onCollectionChanged += t.handle_event
        c.add(11)
        assert t.kwargs['collection'] == c

    def test_onCollectionChanged_remove(self):
        c = ImmediateObservableCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t = self.Tester()
        c.onCollectionChanged += t.handle_event
        c.remove(1)
        assert t.kwargs['collection'] == c

    def test_ItemAdded(self):
        c = ImmediateObservableCollection(1, 2, 3, 4)
        t = self.Tester()

        c.onItemAdded += t.handle_event
        c.add(1)
        assert t.kwargs['collection'] == c
        assert t.args == (1, 4)

    def test_ItemRemoved(self):
        c = ImmediateObservableCollection(1, 2, 3, 4)
        t = self.Tester()
        c.onItemRemoved += t.handle_event
        c.remove(1)
        assert t.kwargs['collection'] == c
        assert t.args == (1, 0)

    def test_ViewChanged(self):
        v = ViewCollection(5, 8, 2, synchronous=True)
        t = self.Tester()
        v.onViewChanged += t.handle_event
        v.update_filter(lambda x: x < 5)
        assert t.kwargs['collection'] == v


class TestViewCollection(TestCase):
    def test_base_binding(self):
        t = TestTarget()
        c = ViewCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t < bind() < c
        t.update_bindings()
        assert t.values == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    def test_base_binding_auto_update_add(self):
        t = TestTarget()
        c = ViewCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t < bind() < c
        c.add(11)
        assert t.values == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)

    def test_base_binding_auto_update_remove(self):
        t = TestTarget()
        c = ViewCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t < bind() < c
        c.remove(5)
        assert t.values == (1, 2, 3, 4, 6, 7, 8, 9, 10)

    def test_base_binding_force(self):
        t = TestTarget()
        c = ViewCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t < bind() < c
        c._internal_collection = ['a', 'b', 'c']
        c.update_bindings()
        assert t.values == ('a', 'b', 'c')

    def test_base_binding_clear(self):
        t = TestTarget()
        c = ViewCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t < bind() < c
        c.update_bindings()
        assert t.values == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        c.clear()
        assert t.values == ()

    def test_base_binding_sort(self):
        t = TestTarget()
        c = ViewCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t < bind() < c
        c.update_bindings()
        assert t.values == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        c.sort(reverse=True)
        assert t.values == (10, 9, 8, 7, 6, 5, 4, 3, 2, 1)

    def test_iter(self):
        c = ViewCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        result = []
        for item in c: result.append(item)
        assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_filter(self):
        t = TestTarget()
        c = ViewCollection(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        t < bind() < c
        t.update_bindings()
        assert t.values == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        c.update_filter(lambda x: x % 2 == 0)
        assert t.values == (2, 4, 6, 8, 10)
