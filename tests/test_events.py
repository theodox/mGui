'''
Created on Mar 13, 2014

@author: stevetheodore
'''
import unittest
import mGui.events as events


class TestWeakRefs(unittest.TestCase):


    def test_free_method(self):
        def example (*args, **kwargs):
            return -99
        wr = events.WeakMethod(example)
        assert isinstance(wr, events.WeakMethodFree)
        
    def test_free_method_works(self):
        def example (*args, **kwargs):
            return -99
        wr = events.WeakMethod(example)
        assert  wr() == -99
        
    def test_free_method_excepts_on_dead_ref(self):
        def example (*args, **kwargs):
            return -99
        wr = events.WeakMethod(example)
        del(example)
        self.assertRaises(events.DeadReferenceError, wr)
    
    class bound_tester(object):
        def example(self):
            return 111
    
    def test_bound_method(self):
        b = self.bound_tester()
        
        wr = events.WeakMethod(b.example)
        assert isinstance(wr, events.WeakMethodBound)
        
    def test_bound_method_works(self):
        b = self.bound_tester()
        wr = events.WeakMethod(b.example)
        assert  wr() == 111
        
    def test_bound_method_excepts_on_dead_ref(self):
        b = self.bound_tester()
        wr = events.WeakMethod(b.example)
        del(b)
        self.assertRaises(events.DeadReferenceError, wr)
    
    def test_bound_method_DOES_NOT_except_on_dead_method_ref(self):
        '''
        you can't 'delete' a bound method, even if you overwrite it's name
        in a particular instance. bound methods work like descriptors under
        the hood.
        '''
        b = self.bound_tester()
        wr = events.WeakMethod(b.example)
        b.example = lambda x: 121
        try:
            wr()
        except events.DeadReferenceError:
            self.fail('this should not raise')
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()