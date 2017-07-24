"""
Observable.py
@author: stevetheodore
"""
import itertools
from collections import MutableSequence, Sequence

from mGui.bindings import BindableObject
from mGui.events import MayaEvent, Event


class ObservableCollection(MutableSequence, BindableObject):
    """
    Encapsulates a collection suitable for data binding. The contents are
    managed internally but visible to other classes as the Contents property

    The collection emits events when it is updated:

       * onItemAdded(item, collection = self) for each item added
       * onItemRemoved(item, collection = self) for each item removed
       * onCollectionChanged(collection = self) for all other changes

    This collections outgoing data bindings will be updated automatically on
    these events as well, so it's not necessary to explicitly handle them
    although that can be done if you need more control over the changes.

    NOTE: it's a Bad Idea(tm) to mess directly with the internal collection. The
    bindable version of it a tuple (so it's immutable). The intended use is for
    display of a list, not list management!

    Inherits methods from BindableObject, so you can manually trigger an update with update_bindings
    """

    _BIND_SRC = 'contents'
    _BIND_TGT = None

    def __init__(self, *items):
        self._internal_collection = [i for i in items]
        self.onCollectionChanged = MayaEvent(collection=self)
        self.onItemAdded = MayaEvent(collection=self)
        self.onItemRemoved = MayaEvent(collection=self)

    @property
    def contents(self):
        """
        The contents of the collection.  Bindable.
        """
        return tuple(self)

    @property
    def count(self):
        """
        The number of items in the collection. Bindable.
        """
        return len(self)

    def add(self, *additions):
        """
        Add items to the collection, with notifications.
        """
        self.extend(additions)

    def add_group(self, *args):
        """
        Add everything in <args>, but only fire the onCollectionChanged event once
        """
        self._internal_collection.extend(args)
        self.update_bindings()
        self.onCollectionChanged(added=True)

    def insert(self, index, item):
        """
        Add <item> at position <index>
        """
        self._internal_collection.insert(index, item)
        self.onItemAdded(item, index)
        self.update_bindings()
        self.onCollectionChanged(added=True)

    def clear(self):
        """
        Clear the collection
        """
        del self._internal_collection[:]
        self.update_bindings()
        self.onCollectionChanged(cleared=True)

    def sort(self, comp=None, key=None, reverse=False):
        """
        Sort the collection with the supplied comparison, key and reverse
        arguments (see list.sort)
        """
        self._internal_collection.sort(comp, key, reverse)
        self.update_bindings()
        self.onCollectionChanged(sorted=True)

    def __getitem__(self, item):
        return self._internal_collection.__getitem__(item)

    def __setitem__(self, index, item):
        self._internal_collection.__setitem__(index, item)
        self.onItemAdded(item, index)
        self.update_bindings()
        self.onCollectionChanged(added=True)

    def __delitem__(self, index):
        self.onItemRemoved(self[index], index)
        self._internal_collection.__delitem__(index)
        self.update_bindings()
        self.onCollectionChanged(removed=True)

    def __len__(self):
        return len(self._internal_collection)

    def reverse(self):
        self._internal_collection.reverse()
        self.update_bindings()
        self.onCollectionChanged(sorted=True)


class ImmediateObservableCollection(ObservableCollection):


    def __init__(self, *items):
        super(ImmediateObservableCollection, self).__init__(*items)
        self.onCollectionChanged = Event(collection=self)
        self.onItemAdded = Event(collection=self)
        self.onItemRemoved = Event(collection=self)


class ViewCollection(ObservableCollection):
    """
    An ObservableCollection with a filter (a predicate function like the ones
    used in a built-in python filter expression).  Changing the filter
    expression updates the 'view', which is the current filtered version of the
    underlying container.

    The class exposes the same events as ObservableCollection, as well as a
    viewChanged event which triggers when the filter is changed
    """
    _BIND_SRC = 'view'

    def __init__(self, *items, **kwargs):
        self._max_size = kwargs.pop('limit', 0)
        synchronous = kwargs.pop('synchronous', False)
        super(ViewCollection, self).__init__(*items)
        self.onViewChanged = MayaEvent(collection=self)
        if synchronous:
            self.onViewChanged = Event(collection=self)

        self._filter = lambda p: p
        self._last_count = len(self._internal_collection)
        self._truncated = False

    @property
    def view(self):
        """
        Returns a tuple of all the items in this collection which pass the
        current filter. Bindable.
        """
        filtered = itertools.ifilter(self._filter, self._internal_collection)
        result = None
        if self._max_size > 0:
            result = tuple(itertools.islice(filtered, self._max_size))
        else:
            result = tuple(filtered)
        self._last_count = len(result)
        self._truncated = len(result) == self._max_size
        return result

    @property
    def viewCount(self):
        """
        The number of items currently passing the filter. Bindable
        """
        return self._last_count

    @property
    def limit(self):
        return self._max_size

    @property
    def is_truncated(self):
        return self._truncated

    def update_filter(self, filter_fn):
        """
        Change the filter expression. This will trigger a ViewChanged event
        """
        if not filter_fn:
            self._filter = lambda p: p
        else:
            self._filter = filter_fn

        self._last_count = len(self.view)
        self.update_bindings()
        self.onViewChanged()

    def __getitem__(self, item):
        return self.view.__getitem__(item)


class BoundCollection(Sequence, BindableObject):
    """
    An iterable object which can be bound to a collection. When the source
    collection updates, the BoundCollection will fire appropriate update
    callbacks.

    """
    _BIND_TGT = 'set_collection'

    def __init__(self):
        self._internal_collection = ()
        self.onCollectionChanged = MayaEvent()  # these are MayaEvents so they are thread safe... we hope
        self.widgetCreated = MayaEvent()

    def set_collection(self, new_contents):
        self._internal_collection = tuple([i for i in new_contents])
        self.onCollectionChanged()

    def __iter__(self):
        for item in self._internal_collection:
            yield item

    @property
    def contents(self):
        for item in self._internal_collection:
            yield item

    @property
    def count(self):
        return len(self)

    def __getitem__(self, item):
        return self._internal_collection[item]

    def __len__(self):
        return len(self._internal_collection)


class ImmediateBoundCollection(BoundCollection):

    _BIND_TGT = 'set_collection'

    def __init__(self):
        self._internal_collection = ()
        self.onCollectionChanged = Event()  # these are MayaEvents so they are thread safe... we hope
        self.onWidgetCreated = Event()
