"""
Created on Mar 13, 2014

@author: stevetheodore
"""
import mGui.events as events
import unittest


class TestWeakRefs(unittest.TestCase):
    def test_free_method(self):
        def example(*args, **kwargs):
            return -99

        wr = events.get_weak_reference(example)
        assert isinstance(wr, events.WeakMethodFree)

    def test_free_method_works(self):
        def example(*args, **kwargs):
            return -99

        wr = events.get_weak_reference(example)
        assert wr() == -99

    def test_free_method_excepts_on_dead_ref(self):
        def example(*args, **kwargs):
            return -99

        wr = events.get_weak_reference(example)
        del example
        self.assertRaises(events.DeadReferenceError, wr)

    def test_free_method_ids_are_stable(self):
        def example(*args, **kwargs):
            return -99

        def example2(*args, **kwargs):
            return -99

        wr = events.get_weak_reference(example)
        wr2 = events.get_weak_reference(example)
        wr3 = events.get_weak_reference(example2)
        wr4 = events.get_weak_reference(example2)
        assert wr.ID == wr2.ID
        assert wr3.ID == wr4.ID
        assert wr.ID != wr4.ID

    class bound_tester(object):
        def example(self):
            return 111

    def test_bound_method(self):
        b = self.bound_tester()

        wr = events.get_weak_reference(b.example)
        assert isinstance(wr, events.WeakMethodBound)

    def test_bound_method_works(self):
        b = self.bound_tester()
        wr = events.get_weak_reference(b.example)
        assert wr() == 111

    def test_bound_method_excepts_on_dead_ref(self):
        b = self.bound_tester()
        wr = events.get_weak_reference(b.example)
        del b
        self.assertRaises(events.DeadReferenceError, wr)

    def test_bound_method_ids_are_stable(self):
        b = self.bound_tester()
        b2 = self.bound_tester()
        wr = events.get_weak_reference(b.example)
        wr2 = events.get_weak_reference(b.example)
        wr3 = events.get_weak_reference(b2.example)
        wr4 = events.get_weak_reference(b2.example)
        assert wr.ID == wr2.ID
        assert wr3.ID == wr4.ID
        assert wr.ID != wr4.ID

    def test_bound_method_DOES_NOT_except_on_dead_method_ref(self):
        """
        you can't 'delete' a bound method, even if you overwrite it's name
        in a particular instance. bound methods work like descriptors under
        the hood.
        """
        b = self.bound_tester()
        wr = events.get_weak_reference(b.example)
        b.example = lambda x: 121
        try:
            wr()
        except events.DeadReferenceError:
            self.fail("this should not raise")


class TestEvents(unittest.TestCase):
    class bound_tester(object):
        DATA = []

        def example(self, *args, **kwargs):
            self.DATA.append("OK")

    def test_basic_event(self):
        sample_data = []

        def handle(*args, **kwargs):
            sample_data.append("OK")

        test = events.Event()
        test += handle
        test()
        assert "OK" in sample_data

    def test_derefencing(self):
        sample_data = []

        def handle(*args, **kwargs):
            sample_data.append("OK")

        test = events.Event()
        test += handle
        test()
        assert "OK" in sample_data
        test -= handle
        sample_data.remove("OK")
        test()
        assert "OK" not in sample_data

    def test_bound_derefencing(self):
        sample_data = []
        b = self.bound_tester()

        test = events.Event()
        test += b.example
        test()
        assert "OK" in self.bound_tester.DATA
        test -= b.example
        self.bound_tester.DATA.remove("OK")
        test()
        assert not "OK" in self.bound_tester.DATA

    def test_stash(self):
        sample_data = []

        def handle(*args, **kwargs):
            sample_data.append("OK")

        class Stash(object):
            pass

        stash = Stash()

        test = events.Event()
        test += handle, stash
        del handle
        test()
        assert "OK" in sample_data

    def test_stash_derefencing(self):
        sample_data = []

        def handle(*args, **kwargs):
            sample_data.append("OK")

        handle_id = id(handle)

        class Stash(object):
            pass

        stash = Stash()

        test = events.Event()
        test += handle, stash
        del handle
        test()
        assert "OK" in sample_data
        handle = getattr(stash, "_sh_{}".format(handle_id))
        sample_data = []
        test -= handle, stash
        test()
        assert "OK" not in sample_data


if __name__ == "__main__":
    unittest.main()
