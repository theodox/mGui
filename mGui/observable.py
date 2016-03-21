"""
Observable.py
@author: stevetheodore
"""
import itertools

from mGui.bindings import BindableObject
from mGui.events import MayaEvent, Event


class ObservableCollection(BindableObject):
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
        return tuple([i for i in self._internal_collection])

    @property
    def count(self):
        """
        The number of items in the collection. Bindable.
        """
        return len(self._internal_collection)

    def add(self, *additions):
        """
        Add items to the collection, with notifications.
        """
        if len(additions):
            for each_new in additions:
                self._internal_collection.append(each_new)
                self.onItemAdded(each_new, len(self._internal_collection) - 1)
            self.update_bindings()
            self.onCollectionChanged(added=True)

    def add_group(self, *args):
        """
        Add everything in <args>, but only fire the onCollectionChanged event once
        """
        for item in args:
            self._internal_collection.append(item)
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

    def remove(self, *delenda):
        """
        Removes items from the collection
        """
        _found = False
        for item in delenda:
            found = self._internal_collection.index(item)
            if found > -1:
                self.onItemRemoved(item, found)
                _found = True
        for item in delenda:
            self._internal_collection.remove(item)
        if _found:  # if this > -1  something was deleted
            self.update_bindings()
            self.onCollectionChanged(removed=True)

    def clear(self):
        """
        Clear the collection
        """
        self._internal_collection = []
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

    def __iter__(self):
        """
        iterates over the contents of the collection
        """
        for item in self._internal_collection:
            yield item

    def __getitem__(self, item):
        return self._internal_collection.__getitem__(item)


class ImmediateObservableCollection(ObservableCollection):
    def __init__(self, *items):
        self._internal_collection = [i for i in items]
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
    viewChanged event which triggers when the filter is chaanged
    """
    _BIND_SRC = 'view'

    def __init__(self, *items, **kwargs):
        self.max_size = kwargs.pop('limit', 0)
        self.synchronous = kwargs.pop('synchronous', False)
        super(ViewCollection, self).__init__(*items)
        self.onViewChanged = MayaEvent(collection=self)
        if self.synchronous:
            self.onViewChanged = Event(collection = self)

        self.filter = lambda p: p
        self._last_count = len(self._internal_collection)
        self._truncated = False

    @property
    def view(self):
        """
        Returns a tuple of all the items in this collection which pass the
        current filter. Bindable.
        """
        filtered = itertools.ifilter(self.filter, self._internal_collection)
        result = None
        if self.max_size > 0:
            result = tuple(itertools.islice(filtered, self.max_size))
        else:
            result = tuple(filtered)
        self._last_count = len(result)
        self._truncated = len(result) == self.max_size
        return result

    @property
    def viewCount(self):
        """
        The number of items currently passing the filter. Bindable
        """
        return self._last_count

    @property
    def limit(self):
        return self.max_size

    @property
    def is_truncated(self):
        return self._truncated

    def update_filter(self, filter_fn):
        """
        Change the filter expression. This will trigger a ViewChanged event
        """
        if not filter_fn:
            self.filter = lambda p: p
        else:
            self.filter = filter_fn

        self._last_count = len(self.view)
        self.update_bindings()
        self.onViewChanged()

    def __getitem__(self, item):
        return self.view.__getitem__(item)


class BoundCollection(BindableObject):
    """
    An iterable object which can be bound to a collection. When the source
    collection updates, the BoundCollection will fire appropriate update
    callbacks.

    The optional conversion argument is a callable which will be run on every
    item being forwarded from the source collection.
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
        return len(self._internal_collection)


class ImmediateBoundCollection(BoundCollection):
    def __init__(self):
        self._internal_collection = ()
        self.onCollectionChanged = Event()  # these are MayaEvents so they are thread safe... we hope
        self.onWidgetCreated = Event()
